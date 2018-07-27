#!/usr/bin/python
""" Simple http/https server """

import BaseHTTPServer
import SimpleHTTPServer
import ssl



SERVER = BaseHTTPServer.HTTPServer(('localhost', 4443), SimpleHTTPServer.SimpleHTTPRequestHandler)
SERVER.socket = ssl.wrap_socket(SERVER.socket, certfile='/opt/cfssl/pki/crt/cert.pem',
                                keyfile='/opt/cfssl/pki/key/cert-key.pem',
                                server_side=True)
SERVER.serve_forever()
