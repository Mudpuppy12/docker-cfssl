# Docker PKI server using cfssl
I needed a way to generate client certificates from an internal CA on demand. I was sick
of generating openssl csr's, then signing them with a multi-step process of commands I always
have to look up.

This process is much quicker. A client certificate is requested for the docker-cfssl PKI server. The client can be anywhere on the network, provided it can talk to the pki server.

The PKI server  will then return a signed certificate back to the client, provided it passes the correct API-KEY

You should change the API-KEY, if you planning on using these configs.

## Notes

You will need the cfssl and cfssljson binaries on your client to talk to the api-server.
Head over to https://github.com/cloudflare/cfssl to install. Stick the binaries them into a artifactory, or use fpm and make an rpm for your internal repos.

Use ansible to grab the client, then create certs during service installs. That's my attack
plan

You will want to fix up the docker-compose.yml with the correct file paths to the certificates.

The example shell scripts should give you an idea how to use this setup. 