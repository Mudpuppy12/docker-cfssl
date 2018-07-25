#!/usr/bin/python
# Beginings of a toolset to examine certificates that are deployed. The goal is to 
# 1. Remove duplicate signing requests with same common name
# 2. Check expiration dates to alert on common names close to expirting.

import json
import subprocess
import sqlite3
import pprint


db=sqlite3.connect('/opt/src/cfssl/api-server/certs.db')

cursor = db.cursor()

#cursor.execute('''SELECT serial_number, pem, max(expiry) FROM certificates''')
#cursor.execute('''SELECT pem, expiry FROM certificates WHERE expiry not in (SELECT max(expiry) FROM certificates)''')

cursor.execute('''SELECT serial_number, pem, expiry FROM certificates''')
results = cursor.fetchall()
print len(results)


# Build a dictionary with serial as key with information decoded from the PEM.
data={}

for row in results:

   p = subprocess.Popen(['/opt/cfssl/cfssl-certinfo','-cert','-'],stdin=subprocess.PIPE, stdout=subprocess.PIPE)
   p.stdin.write(row[1])
   (output,err) = p.communicate()
   tmp=json.loads(output)
   
   # Lets trim the output a bit and put the data in things we want:
   data[row[0]]={
       'expires': tmp['not_after'],
       'common_name':tmp['subject']['common_name']
   }

