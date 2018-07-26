#!/usr/bin/python
# Beginings of a toolset to examine certificates that are deployed.

import json
import subprocess
import sqlite3
import argparse
import pprint
import datetime
import arrow

# Using arrow for ISO 8601 date manipulation

def load_data(database):
    db=sqlite3.connect(database)
    
    cursor = db.cursor()

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

    db.close()
    return(data,old_serials,len(results))
def list_certs(data):
    for cert in data:
        print('CN={}, Serial={}, Expires={}').format(cert,data[cert]['serial'],data[cert]['expires'])
def expire_ndays(data,ndays):

    for cert in data:
        delta = arrow.get(data[cert]['expires']) - arrow.utcnow()
        if delta.days <= ndays:
            print('{} will expire in {} days').format(cert,delta.days) 
        
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
        help='Show certificates that will expire in X days',
        required=False,
        type=int,
        default=30,
    )

     parser.add_argument(
        '-cd',
        '--dupes',
        help='Count the number of duplicate certificates',
        required=False,
        action='store_true'
    )

     parser.add_argument(
        '-db',
        '--database',
        help='Database file to use, Default: [ %(default)s ]',
        required=False,
        default= '/opt/src/cfssl/api-server/certs.db'
    )

     return vars(parser.parse_args())

def main():
    user_args = args()

    if user_args['list']:
        (data, dups, size) = load_data(user_args['database'])
        list_certs(data)
    if user_args['count']:
        (data, dups, size) = load_data(user_args['database'])
        print('There are {} entries in the database.').format(size)
    if user_args['dupes']:
        (data, dups, size) = load_data(user_args['database'])
        print('There are {} duplicate entries in the database.').format(len(dups)+1)
    if user_args['ndays']:
        (data, dups, size) = load_data(user_args['database'])
        expire_ndays(data,user_args['ndays'])

if __name__ == "__main__":
    main()


