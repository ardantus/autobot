#!/usr/bin/env python3
import sys
import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import io
import urllib.request

# Add piper to path
sys.path.insert(0, '/app/piper/src')

# Ensure espeakbridge.so is available (restore from backup if needed)
if os.path.exists('/app/lib/espeakbridge.so') and not os.path.exists('/app/piper/src/piper/espeakbridge.so'):
    import shutil
    shutil.copy('/app/lib/espeakbridge.so', '/app/piper/src/piper/espeakbridge.so')
    print("Restored espeakbridge.so from backup", flush=True)

# Check if model exists in mounted volume (from ./piper folder)
MODEL_PATH_PIPER = "/app/models/id_ID-news_tts-medium"
MODEL_PATH_DEFAULT = "/app/models/id_ID-news_tts-medium"

# Use model from mounted volume if exists, otherwise use default
if os.path.exists(f"{MODEL_PATH_PIPER}.onnx"):
    MODEL_PATH = MODEL_PATH_PIPER
else:
    MODEL_PATH = MODEL_PATH_DEFAULT

MODEL_ONNX = f"{MODEL_PATH}.onnx"
MODEL_JSON = f"{MODEL_PATH}.onnx.json"

def ensure_model():
    """Download model if not exists"""
    if os.path.exists(MODEL_ONNX) and os.path.exists(MODEL_JSON):
        return True
    
    print("Downloading Indonesian voice model (news_tts)...", flush=True)
    try:
        os.makedirs("/app/models", exist_ok=True)
        urllib.request.urlretrieve(
            "https://huggingface.co/rhasspy/piper-voices/resolve/main/id/id_ID/news_tts/medium/id_ID-news_tts-medium.onnx",
            MODEL_ONNX
        )
        urllib.request.urlretrieve(
            "https://huggingface.co/rhasspy/piper-voices/resolve/main/id/id_ID/news_tts/medium/id_ID-news_tts-medium.onnx.json",
            MODEL_JSON
        )
        print("Model downloaded successfully", flush=True)
        return True
    except Exception as e:
        print(f"Error downloading model: {e}", flush=True, file=sys.stderr)
        return False

# Initialize voice
voice = None
try:
    from piper import PiperVoice
    
    if ensure_model():
        # PiperVoice.load() accepts model_path and config_path
        # Provide config_path explicitly
        if os.path.exists(MODEL_ONNX) and os.path.exists(MODEL_JSON):
            voice = PiperVoice.load(MODEL_ONNX, config_path=MODEL_JSON)
            print(f"Piper TTS initialized with model: {MODEL_ONNX}", flush=True)
        else:
            raise FileNotFoundError(f"Model files not found: {MODEL_ONNX} or {MODEL_JSON}")
    else:
        print("Warning: Model not available, TTS will fail", flush=True, file=sys.stderr)
except Exception as e:
    print(f"Error initializing Piper: {e}", flush=True, file=sys.stderr)
    import traceback
    traceback.print_exc(file=sys.stderr)

class TTSHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            print("POST request received", flush=True)
            if voice is None:
                print("Voice is None!", flush=True)
                self.send_response(500)
                self.send_header("Content-Type", "text/plain")
                self.end_headers()
                self.wfile.write(b"TTS not initialized")
                return
            
            content_length = int(self.headers.get("Content-Length", 0))
            print(f"Content-Length: {content_length}", flush=True)
            body = self.rfile.read(content_length)
            data = json.loads(body.decode("utf-8"))
            text = data.get("text", "")
            print(f"Text received: {text}", flush=True)
            
            if not text:
                print("Empty text received", flush=True)
                self.send_response(400)
                self.end_headers()
                return
            
            # Generate audio using PiperVoice API directly
            print(f"Generating TTS for text: {text[:50]}...", flush=True)
            try:
                from piper.config import SynthesisConfig
                
                # Create synthesis config (use defaults)
                syn_config = SynthesisConfig()
                
                # synthesize() returns a generator of AudioChunk objects
                audio_stream = io.BytesIO()
                audio_chunks = []
                
                # Collect all audio chunks from the generator
                sample_rate = None
                for audio_chunk in voice.synthesize(text, syn_config):
                    audio_chunks.append(audio_chunk)
                    if sample_rate is None:
                        sample_rate = audio_chunk.sample_rate
                
                # Write all audio chunks to BytesIO
                for chunk in audio_chunks:
                    audio_stream.write(chunk.audio_int16_bytes)
                
                # Get the raw PCM audio data
                pcm_data = audio_stream.getvalue()
                print(f"PCM data size: {len(pcm_data)} bytes, sample rate: {sample_rate} Hz", flush=True)
                
                if len(pcm_data) == 0:
                    raise Exception("TTS synthesis produced empty audio")
                
                # Create WAV file with proper header
                # WAV file format: RIFF header + fmt chunk + data chunk
                num_channels = 1  # Mono
                sample_width = 2  # 16-bit = 2 bytes
                byte_rate = sample_rate * num_channels * sample_width
                block_align = num_channels * sample_width
                data_size = len(pcm_data)
                file_size = 36 + data_size  # 36 = header size (44 - 8)
                
                # Build WAV header
                wav_header = bytearray()
                # RIFF header
                wav_header.extend(b'RIFF')
                wav_header.extend(file_size.to_bytes(4, 'little'))
                wav_header.extend(b'WAVE')
                # fmt chunk
                wav_header.extend(b'fmt ')
                wav_header.extend((16).to_bytes(4, 'little'))  # fmt chunk size
                wav_header.extend((1).to_bytes(2, 'little'))   # audio format (1 = PCM)
                wav_header.extend(num_channels.to_bytes(2, 'little'))
                wav_header.extend(sample_rate.to_bytes(4, 'little'))
                wav_header.extend(byte_rate.to_bytes(4, 'little'))
                wav_header.extend(block_align.to_bytes(2, 'little'))
                wav_header.extend((sample_width * 8).to_bytes(2, 'little'))  # bits per sample
                # data chunk
                wav_header.extend(b'data')
                wav_header.extend(data_size.to_bytes(4, 'little'))
                
                # Combine header and PCM data
                audio_data = bytes(wav_header) + pcm_data
                print(f"WAV file size: {len(audio_data)} bytes", flush=True)
                    
            except Exception as e:
                print(f"PiperVoice API failed: {e}", flush=True)
                import traceback
                traceback.print_exc(file=sys.stderr)
                # Fallback to browser TTS (return error so browser can use fallback)
                raise Exception(f"TTS synthesis failed: {str(e)}")
            
            # Send audio response
            self.send_response(200)
            self.send_header("Content-Type", "audio/wav")
            self.send_header("Content-Length", str(len(audio_data)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(audio_data)
            
        except Exception as e:
            error_msg = str(e)
            print(f"Error in TTS handler: {error_msg}", flush=True, file=sys.stderr)
            import traceback
            traceback.print_exc(file=sys.stderr)
            try:
                self.send_response(500)
                self.send_header("Content-Type", "text/plain")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(error_msg.encode("utf-8"))
            except:
                pass  # Connection might be closed
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 5000), TTSHandler)
    print("Piper TTS server running on port 5000", flush=True)
    server.serve_forever()
