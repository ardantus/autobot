# AI Voice Assistant

Sebuah aplikasi asisten suara berbasis AI yang ringan dan hemat sumber daya, menggunakan **Llama.cpp Server** untuk menjalankan model AI lokal di browser. Aplikasi ini dirancang khusus untuk sistem dengan RAM terbatas (target: 4GB RAM).

## 🎯 Fitur Utama

- **🎤 Speech-to-Text**: Menggunakan Web Speech API browser untuk konversi suara ke teks
- **🤖 AI Chat**: Integrasi dengan Llama.cpp Server untuk respons AI lokal
- **🔊 Text-to-Speech**: Membacakan respons AI menggunakan Speech Synthesis API
- **💾 Low Memory**: Optimasi untuk sistem dengan RAM terbatas (4GB)
- **🌙 Dark Mode UI**: Antarmuka modern dengan tema gelap
- **🐳 Docker Compose**: Setup mudah dengan containerisasi

## 📋 Requirements

- **Docker** dan **Docker Compose** terinstall
- **Browser modern** yang mendukung:
  - Web Speech API (Chrome, Edge, Safari)
  - Speech Synthesis API
- **Model .gguf** yang kompatibel (disarankan: Qwen2.5-1.5B-Instruct atau model kecil lainnya)

## 🚀 Instalasi & Setup

### 1. Clone atau Download Proyek

```bash
git clone <repository-url>
cd autobot
```

### 2. Download Model AI (WAJIB - Lakukan SEBELUM Build)

**⚠️ PENTING: Model .gguf TIDAK termasuk dalam repository. Anda HARUS download model terlebih dahulu sebelum build dan run!**

#### Langkah-langkah Download:

1. **Buat folder `models/`** (jika belum ada):
   ```bash
   mkdir -p models
   cd models
   ```

2. **Download model** menggunakan salah satu cara berikut:

   **Cara 1: Menggunakan wget/curl** (Direkomendasikan)
   ```bash
   # Untuk Qwen2.5-0.5B (Sangat Ringan - Direkomendasikan untuk 4GB RAM)
   wget https://huggingface.co/TheBloke/Qwen2.5-0.5B-Instruct-GGUF/resolve/main/qwen2.5-0.5b-instruct-q4_k_m.gguf
   
   # Atau untuk Qwen2.5-1.5B (Lebih Baik, tapi butuh lebih banyak RAM)
   wget https://huggingface.co/TheBloke/Qwen2.5-1.5B-Instruct-GGUF/resolve/main/qwen2.5-1.5b-instruct-q4_k_m.gguf
   ```

   **Cara 2: Download manual dari browser**
   - Kunjungi: https://huggingface.co/TheBloke/Qwen2.5-0.5B-Instruct-GGUF/tree/main
   - Klik tombol "Download" pada file `qwen2.5-0.5b-instruct-q4_k_m.gguf`
   - Simpan file ke folder `models/`

3. **Verifikasi file sudah ada**:
   ```bash
   ls -lh models/*.gguf
   ```

**Catatan**: 
- File model harus ada di folder `models/` sebelum menjalankan langkah berikutnya
- Nama file harus sesuai dengan yang ada di `docker-compose.yml` (default: `qwen2.5-0.5b-instruct-q4_k_m.gguf`)
- Jika menggunakan model lain, edit `docker-compose.yml` sesuai nama file model Anda

### 3. Edit docker-compose.yml (Jika Perlu)

Jika Anda menggunakan model dengan nama berbeda dari default, edit `docker-compose.yml`:

```yaml
command: ["./bin/server", "-m", "/models/NAMA_MODEL_ANDA.gguf", "-c", "512", "--host", "0.0.0.0", "--port", "8080"]
```

Ganti `NAMA_MODEL_ANDA.gguf` dengan nama file model yang Anda download.

### 4. Build Docker Image

Setelah model sudah didownload, build Docker image:

```bash
docker-compose build
```

**Catatan**: 
- Build pertama kali mungkin memakan waktu beberapa menit karena perlu mengcompile llama.cpp dari source
- Pastikan model sudah ada di folder `models/` sebelum build

### 5. Jalankan dengan Docker Compose

```bash
# Build services (jika belum)
docker-compose build

# Start services
docker-compose up -d

# Cek status services
docker-compose ps

# Lihat logs
docker-compose logs -f chat-engine
```

**Catatan**: Pastikan model sudah ada di folder `models/` sebelum menjalankan `docker-compose up`!

### 6. Akses Aplikasi

Buka browser dan navigasi ke:
```
http://localhost
```

## 📖 Cara Penggunaan

1. **Klik tombol mikrofon** untuk mulai merekam
2. **Bicara** - aplikasi akan mendeteksi suara Anda
3. **Berhenti berbicara** - transkrip akan muncul otomatis
4. **Tunggu** - AI akan memproses dan memberikan respons
5. **Dengarkan** - respons AI akan dibacakan secara otomatis

### Status Indikator

- **Ready**: Siap menerima input
- **Listening...**: Sedang merekam suara
- **Thinking...**: AI sedang memproses
- **Speaking**: Sedang membacakan respons

## 📁 Struktur Proyek

```
autobot/
├── docker-compose.yml    # Konfigurasi Docker services
├── Dockerfile            # Dockerfile untuk build llama.cpp server
├── models/               # Folder untuk model .gguf
│   └── model.gguf       # Model AI (harus di-download manual)
├── html/                 # Frontend files
│   └── index.html       # Aplikasi web utama
└── README.md            # Dokumentasi ini
```

## ⚙️ Konfigurasi

### Mengubah Model AI

Model yang digunakan dikonfigurasi melalui nama file di folder `models/`. Ganti `model.gguf` dengan model lain yang Anda inginkan.

### Mengubah Parameter RAM

Edit `docker-compose.yml` untuk menyesuaikan penggunaan RAM:

```yaml
command: -m /models/model.gguf -c 512 --host 0.0.0.0 --port 8080
```

- `-c 512`: Context window (512 tokens). Kurangi untuk menghemat RAM lebih banyak.
- Nilai yang disarankan untuk 4GB RAM: `256-512`

### Mengubah Panjang Output AI

Edit `html/index.html`, cari konstanta:

```javascript
const MAX_PREDICT_TOKENS = 100;
```

Kurangi nilai ini untuk output yang lebih pendek dan menghemat CPU.

### Mengubah Port

Edit `docker-compose.yml`:

```yaml
ports:
  - "8080:8080"  # Format: "HOST_PORT:CONTAINER_PORT"
```

Dan update URL di `html/index.html`:

```javascript
const LLAMA_API_URL = "http://localhost:8080/completion";
```

## 🔧 Troubleshooting

### Error: "Cannot connect to Llama.cpp server"

**Solusi:**
1. Pastikan container `chat-engine` berjalan: `docker-compose ps`
2. Cek logs: `docker-compose logs chat-engine`
3. Pastikan model `model.gguf` ada di folder `models/`
4. Restart service: `docker-compose restart chat-engine`

### Error: "Microphone permission denied"

**Solusi:**
1. Izinkan akses mikrofon di browser
2. Refresh halaman setelah memberikan izin
3. Pastikan browser mendukung Web Speech API

### Model tidak dimuat / Error saat start

**Solusi:**
1. Pastikan file `model.gguf` ada dan tidak corrupt
2. Cek ukuran file model (harus sesuai dengan RAM yang tersedia)
3. Cek logs: `docker-compose logs chat-engine`
4. Pastikan format file adalah `.gguf` (bukan `.bin` atau format lain)

### RAM Usage Terlalu Tinggi

**Solusi:**
1. Kurangi context window (`-c` parameter) di docker-compose.yml
2. Gunakan model yang lebih kecil (1.5B atau lebih kecil)
3. Kurangi `MAX_PREDICT_TOKENS` di index.html
4. Pertimbangkan menggunakan model quantized (Q4_K_M, Q5_K_M)

### Speech Recognition Tidak Bekerja

**Solusi:**
1. Pastikan menggunakan browser yang mendukung (Chrome, Edge, Safari)
2. Cek izin mikrofon di browser settings
3. Pastikan mikrofon terhubung dan berfungsi
4. Coba refresh halaman

## 🛠️ Development

### Menjalankan di Development Mode

```bash
# Lihat logs real-time
docker-compose up

# Atau untuk service tertentu
docker-compose logs -f chat-engine
docker-compose logs -f web-server
```

### Stop Services

```bash
docker-compose down
```

### Rebuild Services

```bash
docker-compose down
docker-compose up -d --force-recreate
```

## 📝 Catatan Teknis

### API Endpoint

Aplikasi menggunakan endpoint Llama.cpp Server:
- **URL**: `http://localhost:8080/completion`
- **Method**: POST
- **Format**: ChatML/Qwen template

### Prompt Format

Aplikasi menggunakan format ChatML untuk prompt:
```
<|im_start|>user
{USER_INPUT}
Answer briefly.<|im_end|>
<|im_start|>assistant
```

### Response Format

Llama.cpp Server mengembalikan JSON:
```json
{
  "content": "AI response text here"
}
```

## 🎯 Optimasi untuk Low-Resource Systems

Proyek ini telah dioptimasi untuk sistem dengan RAM terbatas:

1. **Context Window Kecil**: `-c 512` membatasi penggunaan memori
2. **Output Terbatas**: `n_predict: 100` membatasi panjang respons
3. **Non-Streaming**: Mengurangi overhead network
4. **Model Kecil**: Disarankan menggunakan model 1.5B atau lebih kecil

## 📄 License

[Tambahkan license sesuai kebutuhan]

## 🤝 Contributing

[Tambahkan guidelines untuk kontribusi jika diperlukan]

## 📧 Support

Jika mengalami masalah, silakan buat issue di repository atau hubungi maintainer.

## 🙏 Acknowledgments

Proyek ini menggunakan teknologi open-source berikut:

- **[openWakeWord](https://github.com/dscripka/openWakeWord)** - Framework deteksi wake word untuk aktivasi hands-free
- **[Piper TTS](https://github.com/OHF-Voice/piper1-gpl)** - Sistem text-to-speech neural yang cepat dan lokal
- **[llama.cpp](https://github.com/ggerganov/llama.cpp)** - Inference engine untuk model LLaMA yang dioptimalkan untuk CPU

Terima kasih kepada para kontributor proyek-proyek tersebut!

---

**Dibuat dengan ❤️ untuk sistem low-resource**

