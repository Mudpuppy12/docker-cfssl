#!/bin/sh

echo "Creating certificates"
/usr/local/bin/cfssl gencert -initca ca-csr.json | cfssljson -bare ca
rm ca.csr