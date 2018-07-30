gencert
=========

A certificate generation role to aid in creating private keys and certificate signing requests, or
submit a csr to a cfssl pki signing server.

Output is stored in /opt/cfssl/pki/[crt|csr|key] as ansible_fqdn.*

Requirements
------------

For cfssl pki automatic signing and certificate generation you need to have a cfssl pki
server running on the network. Example can be found here https://github.com/Mudpuppy12/docker-cfssl.


Role Variables
--------------
    Setting your PKI server 

    - cfssl_pki:
          url: "http://127.0.0.1"
          port: "8888"
          api_key: "Some Key here"

    Setting the CA root trust certificate from the cfssl_pki server 
    
    - pki_server_CAfile: <certificate>

    Enabling or disabling using a pki server to auto sign a csr
    - gencert_auto: false

      false: It will just generate a csr and key
      true: It will attempt to get a csr signed from the PKI server

    Creating Java Keystores and pkcs12 certificates

    - genkeystore: true
      Must have gencert_auto set to true as well, will create a java keystore and pkcs12 files
      in /opt/cfssl/pki/java and /opt/cfssl/pki/pkcs12

    Setting Java and pkcs12 passwords

    - cfssl_keystore_pass: changit
    
    Setting the CN for the certifiate, default is ansible_fqdn
     - csr_generate_cn: "example.com"

    Setting SAN, default is ansible_fqdn
     - csr_generate_sans:
          - "example.com"
          - "vip.example.com"


    Setting various parts that generate the subject line

      - csr_country | default('US') 
      - csr_loction | default('Austin') 
      - csr_organization | default('MyCompany')
      - csr_orgunit | default('Client Cert')
      - csr_state | default('Texas')

    

Dependencies
------------
You'll need cfssl binary installed on nexus. Java and openssl when messing with creating
keystores on target hosts (keytool needs to be installed)

Example Playbook
----------------
Example playbook which will generate a CSR using ansible_fqdn as the CN, and SANS.
It will not use a pki server to autosign and output is in /opt/cfssl/pki

  - name: Deploy a certificate
  hosts: testbox
  become: yes
  vars:
    - ansible_user: vagrant 
    - gencert_auto: false
  roles:
    - role: gencert

Example of using the api server

  - name: Deploy a certificate
  hosts: testbox
  become: yes
  vars:
    - ansible_user: vagrant #"{{ hosts.ansible_user }}"
    - cfssl_pki:
          url: "http://127.0.0.1"
          port: "8888"
          api_key: "000102030405060708"
    - gencert_auto: true
  roles:
    - role: gencert

Author Information
------------------

dennis@demarco.com