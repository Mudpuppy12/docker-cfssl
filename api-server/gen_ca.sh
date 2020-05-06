#!/bin/sh

echo "Creating certificates"
/usr/local/bin/cfssl gencert -initca ca-csr.json | cfssljson -bare ca
rm ca.csr

echo "Creating API certificate and sign it with your Root CA"
/usr/local/bin/cfssl genkey api-csr.json | cfssljson -bare api
/usr/local/bin/cfssl sign -ca ca.pem -ca-key ca-key.pem api-csr.csr | cfssljson -bare api.pem