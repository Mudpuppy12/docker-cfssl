#!/usr/bin/python
# Beginings of a toolset to examine certificates that are deployed. The goal is to 
# 1. Remove duplicate signing requests with same common name
# 2. Check expiration dates to alert on common names close to expirting.

import json
import subprocess
import sqlite3
import argparse
import pprint

def load_data():
    db=sqlite3.connect('/opt/src/cfssl/api-server/certs.db')
    
    cursor = db.cursor()
    
    #cursor.execute('''SELECT serial_number, pem, max(expiry) FROM certificates''')
    #cursor.execute('''SELECT pem, expiry FROM certificates WHERE expiry not in (SELECT max(expiry) FROM certificates)''')
    
    cursor.execute('''SELECT serial_number, pem, expiry FROM certificates''')
    results = cursor.fetchall()
    
    
    # Build a dictionary with serial as key with information decoded from the PEM.
    data={}
    old_serials=[]
    for row in results:
       p = subprocess.Popen(['/opt/cfssl/cfssl-certinfo','-cert','-'],stdin=subprocess.PIPE, stdout=subprocess.PIPE)
       p.stdin.write(row[1])
       (output,err) = p.communicate()
       tmp=json.loads(output)
       
       # Lets trim the output a bit we are interested in unique common names with the latest expiration
       
       key = tmp['subject']['common_name']
       
       if not data.has_key(key):    # No key entry, first seeing this so let's insert into our dict
           data[key]= {
           'expires': tmp['not_after'],
           'serial': row[0]
          } 
       elif tmp['not_after'] > data[key]['expires']:   # We already have an entry, lets check expiration. ISO 8601 can be easily string compared.
           old_serials.append(data[key]['serial'])     # Let's keep track of old serials, should we care to clean them out later.
    
           data[key]= {
           'expires': tmp['not_after'],
           'serial': row[0]
          } 
    pprint.pprint(data)
    db.close()

def args(): 
     parser = argparse.ArgumentParser(
        usage='%(prog)s',
        description='cfssl database tools',
        epilog='Version 1.0'
    )

     parser.add_argument(
        '-l',
        '--list',
        help='list unique CN certificates and expiration date',
        required=False,
        action='store_true'
    )

     parser.add_argument(
        '-d',
        '--delete',
        help='Delete duplicate common names, keep only latest expiration date in database',
        required=False,
        action='store_true'
    )

     parser.add_argument(
        '-c',
        '--count',
        help='Count number total entries in database',
        required=False,
        action='store_true'
    )
     parser.add_argument(
        '-n',
        '--ndays',
        help='Show certificates that will expire in X days Default: [ %(default)s ]',
        required=False,
        default='30'
    )

     parser.add_argument(
        '-cd',
        '--dupes',
        help='Count the number of duplicate certificates',
        required=False,
        action='store_true'
    )

     return vars(parser.parse_args())

def main():
    user_args = args()

    if user_args['list']:
        load_data()

if __name__ == "__main__":
    main()


