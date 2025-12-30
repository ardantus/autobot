FROM ubuntu:22.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Clone llama.cpp
WORKDIR /app
RUN git clone --depth 1 https://github.com/ggerganov/llama.cpp.git .

# Build server using CMake (llama.cpp now uses CMake instead of Make)
# Disable CURL since we don't need it for local server
# Build all targets (server will be included)
RUN mkdir -p build && cd build && \
    cmake .. -DCMAKE_BUILD_TYPE=Release -DLLAMA_CURL=OFF && \
    cmake --build . --config Release -j$(nproc)

# Find and verify server binary location
# Binary is named llama-server, not server
RUN if [ -f /app/build/bin/llama-server ]; then \
        echo "Server binary found at: /app/build/bin/llama-server" && \
        ln -sf /app/build/bin/llama-server /app/build/bin/server; \
    else \
        echo "ERROR: llama-server binary not found!" && \
        echo "Available executables:" && \
        find /app/build/bin -type f -executable | head -20 && \
        exit 1; \
    fi

# Expose port
EXPOSE 8080

# Default command (can be overridden in docker-compose)
WORKDIR /app/build
CMD ["./bin/server", "-m", "/models/model.gguf", "-c", "512", "--host", "0.0.0.0", "--port", "8080"]
