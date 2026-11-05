
#!/bin/bash

set -e

mkdir -p data

SIZE=1048576

echo "Generating data using Linux /dev/urandom..."

head -c "$SIZE" /dev/urandom > data/linux_urandom.bin

echo "Generating data using OpenSSL RAND..."

openssl rand -out data/openssl_random.bin "$SIZE"

echo ""
echo "Generation completed."

wc -c data/linux_urandom.bin
wc -c data/openssl_random.bin
