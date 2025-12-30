# Rekomendasi Model AI untuk Bahasa Indonesia

Dokumen ini berisi daftar model AI dalam format GGUF yang mendukung bahasa Indonesia dan cocok untuk sistem low-resource (4GB RAM).

## 🎯 Model yang Direkomendasikan

### 1. **Qwen2.5-0.5B-Instruct** (Saat ini digunakan) ⭐
- **Ukuran**: ~0.5B parameters
- **Format**: GGUF (Q4_K_M, Q5_K_M, dll)
- **Bahasa**: Multilingual termasuk Bahasa Indonesia
- **RAM**: ~1-2GB
- **Download**: 
  - Hugging Face: `Qwen/Qwen2.5-0.5B-Instruct-GGUF`
  - TheBloke: `TheBloke/Qwen2.5-0.5B-Instruct-GGUF`
- **Kelebihan**: 
  - Sangat ringan, cocok untuk 4GB RAM
  - Mendukung bahasa Indonesia dengan baik
  - Response cepat
- **Kekurangan**: 
  - Kualitas respons mungkin lebih sederhana dibanding model besar

### 2. **Qwen2.5-1.5B-Instruct** ⭐⭐⭐
- **Ukuran**: ~1.5B parameters
- **Format**: GGUF (Q4_K_M recommended)
- **Bahasa**: Multilingual termasuk Bahasa Indonesia
- **RAM**: ~2-3GB
- **Download**: 
  - Hugging Face: `Qwen/Qwen2.5-1.5B-Instruct-GGUF`
  - TheBloke: `TheBloke/Qwen2.5-1.5B-Instruct-GGUF`
- **Kelebihan**: 
  - Keseimbangan baik antara ukuran dan kualitas
  - Mendukung bahasa Indonesia dengan baik
  - Masih cocok untuk 4GB RAM dengan quantization Q4
- **Kekurangan**: 
  - Lebih besar dari 0.5B

### 3. **Gemma 1B - Ringkasan Bahasa Indonesia** 🇮🇩
- **Ukuran**: ~1B parameters
- **Format**: GGUF
- **Bahasa**: Bahasa Indonesia (fine-tuned khusus)
- **RAM**: ~1-2GB
- **Download**: 
  - Hugging Face: `dwili/gemma3-1b-ringkasan-bahasa-indo-gguf`
- **Kelebihan**: 
  - Di-fine-tune khusus untuk bahasa Indonesia
  - Sangat ringan
  - Fokus pada tugas peringkasan
- **Kekurangan**: 
  - Mungkin kurang baik untuk percakapan umum
  - Fokus pada peringkasan teks

### 4. **MiaLatte-Indo-Mistral-7B** 🇮🇩
- **Ukuran**: ~7B parameters (quantized)
- **Format**: GGUF (Q4_K_M)
- **Bahasa**: Bahasa Indonesia (fine-tuned khusus)
- **RAM**: ~4-5GB (dengan Q4_K_M)
- **Download**: 
  - Cari di Hugging Face: `MiaLatte-Indo-Mistral-7B-GGUF`
- **Kelebihan**: 
  - Di-optimalkan khusus untuk bahasa Indonesia
  - Kualitas respons lebih baik
  - Mendukung instruksi dalam bahasa Indonesia
- **Kekurangan**: 
  - Lebih besar, mungkin terlalu besar untuk 4GB RAM
  - Perlu quantization yang lebih agresif (Q3_K_M)

### 5. **Qwen2.5-3B-Instruct** (Jika RAM cukup)
- **Ukuran**: ~3B parameters
- **Format**: GGUF (Q4_K_M)
- **Bahasa**: Multilingual termasuk Bahasa Indonesia
- **RAM**: ~3-4GB
- **Download**: 
  - Hugging Face: `Qwen/Qwen2.5-3B-Instruct-GGUF`
- **Kelebihan**: 
  - Kualitas lebih baik dari 1.5B
  - Masih bisa di-squeeze untuk 4GB RAM
- **Kekurangan**: 
  - Mungkin terlalu besar untuk sistem 4GB

## 📥 Cara Download Model

### Metode 1: Menggunakan Hugging Face CLI

```bash
# Install huggingface-cli
pip install huggingface-hub

# Download model (contoh: Qwen2.5-1.5B-Instruct Q4_K_M)
huggingface-cli download TheBloke/Qwen2.5-1.5B-Instruct-GGUF \
  qwen2.5-1.5b-instruct-q4_k_m.gguf \
  --local-dir ./models \
  --local-dir-use-symlinks False
```

### Metode 2: Download Manual dari Hugging Face

1. Kunjungi: https://huggingface.co/TheBloke/Qwen2.5-1.5B-Instruct-GGUF
2. Pilih file `.gguf` yang diinginkan (disarankan Q4_K_M untuk 4GB RAM)
3. Download file tersebut
4. Letakkan di folder `./models/`
5. Rename sesuai kebutuhan atau update `docker-compose.yml`

### Metode 3: Menggunakan wget/curl

```bash
# Contoh download Qwen2.5-1.5B-Instruct Q4_K_M
cd models
wget https://huggingface.co/TheBloke/Qwen2.5-1.5B-Instruct-GGUF/resolve/main/qwen2.5-1.5b-instruct-q4_k_m.gguf
```

## ⚙️ Konfigurasi untuk Bahasa Indonesia

### Update docker-compose.yml

Setelah download model, update `docker-compose.yml`:

```yaml
command: ["./bin/server", "-m", "/models/nama-model-anda.gguf", "-c", "512", "--host", "0.0.0.0", "--port", "8080"]
```

### Update Prompt Template (jika perlu)

Untuk model yang sudah fine-tuned untuk bahasa Indonesia, prompt template default biasanya sudah cukup. Tapi jika ingin lebih optimal, bisa update di `html/index.html`:

```javascript
function formatPrompt(userInput) {
    // Untuk model yang mendukung bahasa Indonesia
    return `<|im_start|>user\n${userInput}\nJawablah dengan singkat dalam bahasa Indonesia.<|im_end|>\n<|im_start|>assistant\n`;
}
```

## 📊 Perbandingan Model

| Model | Ukuran | RAM | Kualitas ID | Kecepatan | Rekomendasi |
|-------|--------|-----|--------------|-----------|-------------|
| Qwen2.5-0.5B | 0.5B | 1-2GB | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ✅ Untuk 4GB |
| Qwen2.5-1.5B | 1.5B | 2-3GB | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ✅✅ Paling direkomendasikan |
| Gemma 1B Indo | 1B | 1-2GB | ⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ Untuk peringkasan |
| Mistral 7B Indo | 7B | 4-5GB | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⚠️ Mungkin terlalu besar |
| Qwen2.5-3B | 3B | 3-4GB | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⚠️ Batas untuk 4GB |

## 🎯 Rekomendasi Final

**Untuk sistem 4GB RAM:**
1. **Pilihan Utama**: Qwen2.5-1.5B-Instruct (Q4_K_M) - keseimbangan terbaik
2. **Pilihan Ringan**: Qwen2.5-0.5B-Instruct (Q4_K_M) - jika RAM sangat terbatas
3. **Pilihan Khusus**: Gemma 1B Ringkasan - jika fokus pada peringkasan teks

## 🔗 Link Download Langsung

### Qwen2.5-1.5B-Instruct (Direkomendasikan)
- **Q4_K_M** (Recommended): https://huggingface.co/TheBloke/Qwen2.5-1.5B-Instruct-GGUF/tree/main
- **Q5_K_M** (Better quality, lebih besar): https://huggingface.co/TheBloke/Qwen2.5-1.5B-Instruct-GGUF/tree/main

### Qwen2.5-0.5B-Instruct (Saat ini digunakan)
- **Q4_K_M**: https://huggingface.co/TheBloke/Qwen2.5-0.5B-Instruct-GGUF/tree/main

### Gemma 1B Ringkasan Bahasa Indonesia
- https://huggingface.co/dwili/gemma3-1b-ringkasan-bahasa-indo-gguf

## 📝 Catatan

1. **Quantization**: Semakin kecil quantization (Q4, Q3), semakin kecil ukuran file dan penggunaan RAM, tapi kualitas sedikit menurun
2. **Context Window**: Parameter `-c 512` di docker-compose sudah optimal untuk 4GB RAM
3. **Testing**: Setelah download model baru, test dulu dengan pertanyaan sederhana dalam bahasa Indonesia

## 🚀 Quick Start

```bash
# 1. Download model (contoh: Qwen2.5-1.5B Q4_K_M)
cd models
wget https://huggingface.co/TheBloke/Qwen2.5-1.5B-Instruct-GGUF/resolve/main/qwen2.5-1.5b-instruct-q4_k_m.gguf

# 2. Update docker-compose.yml
# Ganti nama file di command menjadi: qwen2.5-1.5b-instruct-q4_k_m.gguf

# 3. Restart container
docker compose down
docker compose up -d

# 4. Test dengan pertanyaan bahasa Indonesia di browser
```

---

**Tips**: Mulai dengan Qwen2.5-1.5B-Instruct Q4_K_M untuk keseimbangan terbaik antara kualitas dan penggunaan RAM!

