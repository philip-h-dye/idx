#!/usr/bin/env python

"""
Usage: id [OPTION]... [USER]
Print user and group information for the specified USER,
or (when USER omitted) for the current user.

  -a             ignore, for compatibility with other versions
  -Z, --context  print only the security context of the process
  -g, --group    print only the effective group ID
  -G, --groups   print all group IDs
  -n, --name     print a name instead of a number, for -ugG
  -r, --real     print the real ID instead of the effective ID, with -ugG
  -u, --user     print only the effective user ID
  -z, --zero     delimit entries with NUL characters, not whitespace
                   not permitted in default format
      --help     display this help and exit
      --version  output version information and exit

Enhancements :
  -j, --json     display listing in JSON
  -y, --yaml     display listing in YAML
  -l, --list     display vertical listing without indentation
  -d, --data <d> specifies id output for debugging

Affect of id flags on enhancements :

  -a             ignored
  -Z, --context  no enhancements
  -g, --group    no enhancements
  -G, --groups   Only groups but enhancements applied
  -n, --name     Value modifier, see notes for -u, -g and -G
  -r, --real     Value modifier, see notes for -u, -g and -G
  -u, --user     no enhancements
  -z, --zero     Necessary for '-nG' when gecos contain spaces
      --help     no enhancements
      --version  no enhancements

Without any OPTION, print some useful set of identified information.
  i.e.  uid=<uid>(<gecos>) gid=<gid>(<gecos>) groups=<gid>(<gecos>)...
"""

import sys
import subprocess
import re

import argparse

import json
import yaml

import idx.parser

from prettyprinter import pprint as pp

#------------------------------------------------------------------------------

id_exe = '/usr/bin/id'

#------------------------------------------------------------------------------

# As setuptools' entry point passes nothing, argv must default to sys.argv main
# to work.  Do not use sys.argv inside main since that would break unit tests.

def main(argv=sys.argv) :

    parser = argparse.ArgumentParser (
        description = 'Print user and group information for the specified USER'
        + ', or (when USER omitted) for the current user.'
        , add_help = False )

    parser.add_argument (
        '--json', '-j', action = 'store_true'
        , help='display listing in JSON' )

    parser.add_argument (
        '--yaml', '-y', action = 'store_true'
        , help='display listing in YAML' )

    parser.add_argument (
        '--list', '-l', action = 'store_true'
        , help='display vertical listing without indentation' )

    parser.add_argument (
        '--data', '-d', action = 'store'
        , help='specifies id output for debugging' )

    options, command = parser.parse_known_args(argv[1:])

    if '-a' in command :
        command = list(filter(('-a').__ne__, command))

    if '--help' in command :
        print(__doc__)
        exit ( 0 )

    cmd_str = ''.join(command)
    groups = 'G' in cmd_str or '--groups' in cmd_str
    zero = 'z' in cmd_str or '--zero' in cmd_str
    names = 'n' in cmd_str

    enhanced = ( options.list or options.yaml or options.json ) and ( len(command) == 0 or groups )

    if options.data :
        output = options.data
    else :
        command.insert ( 0, id_exe )
        output = subprocess.check_output ( command ).decode('utf-8')

    if not enhanced :
        print( output )
        return ( 0 )

    if options.list :
        output = re.compile( r'\s+(?=[^()]*\))' ).sub( '<space>', output )
        output = re.compile( r'(\s|,)+' ).sub( '\n', output )
        output = re.compile( r'=' ).sub( '=\n', output )
        output = re.compile( r'<space>' ).sub( ' ', output )
        print ( output )

    if not ( options.yaml or options.json ) :
        return ( 0 )

    # List of group ids or names (if -n/--name specified)
    if groups :
        if names :
            sep = '\0' if zero else ' '
            result = { "groups" : [ { "gecos" : value } for value in output.split(sep) ] }
            del result['groups'][-1]
        else :
            result = { "groups" : [ { "gid" : int(value) } for value in output.split() ] }
    else :
        result = idx.parser.parse(output)

    if options.yaml :
        print( yaml.dump(result, default_flow_style=False, sort_keys=False) )

    if options.json :
        output = json.dumps(result, indent=2)
        print( re.sub('{\n      "', '{ "', output) )

    return ( 0 )

#------------------------------------------------------------------------------
