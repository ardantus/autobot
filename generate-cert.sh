#!/bin/bash

# Script to generate self-signed SSL certificate for HTTPS

CERT_DIR="./certs"
CERT_FILE="$CERT_DIR/cert.pem"
KEY_FILE="$CERT_DIR/key.pem"

# Create certs directory if it doesn't exist
mkdir -p "$CERT_DIR"

# Check if certificate already exists
if [ -f "$CERT_FILE" ] && [ -f "$KEY_FILE" ]; then
    echo "Certificate already exists at $CERT_FILE"
    echo "To regenerate, delete the existing certificate files first."
    exit 0
fi

# Generate self-signed certificate
echo "Generating self-signed SSL certificate..."
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout "$KEY_FILE" \
    -out "$CERT_FILE" \
    -subj "/C=ID/ST=Jakarta/L=Jakarta/O=AutoBot/OU=IT/CN=localhost" \
    -addext "subjectAltName=DNS:localhost,DNS:*.localhost,IP:127.0.0.1,IP:0.0.0.0"

if [ $? -eq 0 ]; then
    echo "✅ Certificate generated successfully!"
    echo "   Certificate: $CERT_FILE"
    echo "   Private Key: $KEY_FILE"
    echo ""
    echo "⚠️  This is a self-signed certificate."
    echo "   Your browser will show a security warning."
    echo "   Click 'Advanced' and 'Proceed to localhost' to continue."
    
    # Set proper permissions
    chmod 644 "$CERT_FILE"
    chmod 600 "$KEY_FILE"
else
    echo "❌ Failed to generate certificate"
    exit 1
fi

