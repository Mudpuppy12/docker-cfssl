#!/bin/sh
/usr/local/bin/cfssl gencert -config config_client.json csr_client.json | cfssljson -bare newcert
rm newcert.csr
