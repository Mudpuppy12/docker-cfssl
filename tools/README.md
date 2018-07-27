# Toolbox

SSLPoke.java
=============
Tool to test java keystores

Usage:
<pre>
java -Djavax.net.ssl.trustStore=/opt/pki/java/keystore.jks -Djavax.net.ssl.trustStorePassword=PASSWORD SSLPoke SERVER PORT
</pre>

simple-srv.py
==============
A simple https server to load certificates to test against with SSLPoke or openssl s_client

