#!/usr/bin/env bash

CERTS_DIR="./certs"
mkdir -p "$CERTS_DIR"

echo "======================================="
echo "Generate certs for IoT"
echo "======================================="


ROOT_CA_KEY="$CERTS_DIR/root_ca.key"
ROOT_CA_PEM="$CERTS_DIR/root_ca.pem"
ROOT_CA_SRL="$CERTS_DIR/root_ca.srl"

if [ -f "$ROOT_CA_KEY" ] && [ -f "$ROOT_CA_PEM" ]; then
  echo "CA already exist: $ROOT_CA_KEY, $ROOT_CA_PEM"
  echo "Skipping generate CA"
else
  echo "Generate private key for CA"
  openssl genpkey -algorithm RSA -out "$ROOT_CA_KEY" -pkeyopt rsa_keygen_bits:2048
  
  echo "Generate root CA"
  openssl req -x509 -new -nodes -key "$ROOT_CA_KEY" -sha256 -days 365 -out "$ROOT_CA_PEM"
  
  echo "1000" > "$ROOT_CA_SRL"
  
  echo "CA: $ROOT_CA_PEM | KEY: $ROOT_CA_KEY"
fi

read -p "Common name (CN) for device: " CN
read -p "Cert valid days (default 365): " VALID_DAYS

VALID_DAYS=${VALID_DAYS:-365}

DEVICE_KEY="$CERTS_DIR/device_${CN}.key"
DEVICE_CSR="$CERTS_DIR/device_${CN}.csr"
DEVICE_PEM="$CERTS_DIR/device_${CN}.pem"

echo "Generate device private key ($DEVICE_KEY)..."
openssl genpkey -algorithm RSA -out "$DEVICE_KEY" -pkeyopt rsa_keygen_bits:2048

echo "Generate CSR ($DEVICE_CSR) with CN=$CN..."
openssl req -new -key "$DEVICE_KEY" -out "$DEVICE_CSR" -subj "/CN=$CN"

echo "Singing device cert"
openssl x509 -req \
  -in "$DEVICE_CSR" \
  -CA "$ROOT_CA_PEM" \
  -CAkey "$ROOT_CA_KEY" \
  -CAserial "$ROOT_CA_SRL" \
  -out "$DEVICE_PEM" \
  -days "$VALID_DAYS"

echo
echo "==========================================="
echo " - Root CA: $ROOT_CA_PEM"
echo " - Root key CA: $ROOT_CA_KEY"
echo " - Device cert: $DEVICE_PEM"
echo " - Device key: $DEVICE_KEY"
echo
echo "Device cert with CN=$CN, valid for: $VALID_DAYS dni."
echo "==========================================="

