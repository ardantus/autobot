#!/usr/bin/env python3
import sys
import asyncio
import websockets
import json
import numpy as np
from openwakeword.model import Model
import os

# Flush output immediately
sys.stdout.flush()
sys.stderr.flush()

# Try to initialize model - openWakeWord will download models automatically if needed
print("Initializing openWakeWord model...", flush=True)
sys.stdout.flush()

try:
    # Use all default models - this will auto-download if needed
    model = Model()  # Use all default models
    print(f"Model initialized successfully with {len(model.models)} models: {list(model.models.keys())}", flush=True)
    sys.stdout.flush()
except Exception as e:
    print(f"Error initializing model: {e}", flush=True, file=sys.stderr)
    import traceback
    traceback.print_exc(file=sys.stderr)
    sys.stderr.flush()
    model = None

async def handle_client(websocket, path):
    print("Client connected")
    if model is None:
        await websocket.send(json.dumps({"error": "Model not available"}))
        return
    try:
        async for message in websocket:
            if isinstance(message, bytes):
                # Convert audio bytes to numpy array (16-bit PCM, 16kHz)
                audio_data = np.frombuffer(message, dtype=np.int16).astype(np.float32) / 32768.0
                
                # Predict wake word
                prediction = model.predict(audio_data)
                
                # Check if wake word detected
                for mdl in model.models.keys():
                    if prediction[mdl] > 0.5:  # Threshold
                        await websocket.send(json.dumps({
                            "wake_word": mdl,
                            "confidence": float(prediction[mdl])
                        }))
            elif isinstance(message, str):
                data = json.loads(message)
                if data.get("action") == "reset":
                    model.reset()
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")
    except Exception as e:
        print(f"Error in handle_client: {e}")

async def main():
    try:
        server = await websockets.serve(handle_client, "0.0.0.0", 8765)
        print("Wake word server running on port 8765", flush=True)
        print(f"Model status: {'Available' if model is not None else 'Not available'}", flush=True)
        sys.stdout.flush()
        await server.wait_closed()
    except Exception as e:
        print(f"Error starting server: {e}", flush=True, file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.stderr.flush()
        raise

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server stopped")
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)

