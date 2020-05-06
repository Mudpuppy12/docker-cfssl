#!/bin/sh
/usr/local/bin/cfssl gencert -config=config_client.json -tls-remote-ca root-ca.pem -profile=default csr_client.json | cfssljson -bare newcert