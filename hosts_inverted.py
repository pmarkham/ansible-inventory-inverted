#!/usr/bin/env python

import os
import sys
import json

if len(sys.argv) != 1:
    if len(sys.argv) != 2 or sys.argv[1] != '--list':
        print "Usage: hosts.py --list"
        exit(1)

inventory_file_name = sys.argv[0].rstrip('.py') + '.ini'

inventory_in = file(inventory_file_name)
inventory_out = {'_meta': { 'hostvars' : {} }}

def add_host(group, host_line):
    host_tokens = host_line.split()
    host = host_tokens[0]
    inventory_out['_meta']['hostvars'][host] = {} 
    if len(host_tokens) > 1:
        host_var = {}
        for token in host_tokens[1:]:
            (var, val) = token.split('=')
            host_var[var] = val
        inventory_out['_meta']['hostvars'][host] = host_var
         
    if not group in inventory_out:
        inventory_out[group] = { 'hosts': [], 'vars': {}, "children": [] }
    inventory_out[group]['hosts'].append(host)

def add_var(group, variable):
    if not group in inventory_out:
        inventory_out[group] = { 'hosts': [], 'vars': {}, "children": [] }
    (var, val) = variable.split('=')
    inventory_out[group]['vars'][var] = val

def add_parent(group, member_of):
    if not member_of in inventory_out:
        inventory_out[member_of] = { 'hosts': [], 'vars': {}, "children": [] }
    inventory_out[member_of]['children'].append(group)
    
line_num = 0
current_state = ''
for line in inventory_in:
    line_num += 1
    line = line.strip()
    if line == '':
       continue
    if line.startswith('#'):
       continue
    if line.startswith('['):
       if not line.endswith(']'):
           print "Line: %4d - Syntax error: '%s' has no trailing ']'" % (line_num, line)
           exit(1)
       current_group = line.replace("[","").replace("]","")
       current_state = 'host'
       if ':vars' in line:
           current_group = current_group.rsplit(":", 1)[0]
           current_state = 'var'
       elif ':parents' in line:
           current_group = current_group.rsplit(":", 1)[0]
           current_state = 'parents'
       elif ':' in line:
        print "Line: %4d - Syntax error: no idea what to do with this line." % (line_num)
        exit(1)
       continue
    if current_state == 'host':
        add_host(current_group, line)
    elif current_state == 'var':
        add_var(current_group, line)
    elif current_state == 'parents':
        add_parent(current_group, line)
    else:
        print "Line: %4d - Syntax error: no idea what to do with this line." % (line_num)
        exit(1)

print json.dumps(inventory_out, sort_keys=True, indent=4, separators=(',', ': '))
