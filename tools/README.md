# Toolbox

SSLPoke.java
=============
Tool to test java keystores

Usage:
java -Djavax.net.ssl.trustStore=/opt/pki/java/keystore.jks -Djavax.net.ssl.trustStorePassword=<password> SSLPoke <server> <port>

simple-srv.py
==============
A simple https server to load certificates to test against with SSLPoke or openssl s_client

