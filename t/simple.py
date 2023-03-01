#!/usr/bin/env python

from idx.parser import parse

def main():

    text = "uid=197697(phdye) gid=197121(None) groups=197697(phdye),197121(None)"

    expect =  { "user"   : { 'uid' : 197697, 'gecos' : "phdye" },
                "group"  : { 'gid' : 197121, 'gecos' : "None" },
                "groups" : [ { 'gid' : 197697, 'gecos' : "phdye" },
                             { 'gid' : 197121, 'gecos' : "None" } ] }

    result = parse(text)

    import json
    print("JSON :")
    print( json.dumps(result, indent=4) )
    print()

    import yaml
    print("YAML :")
    print( yaml.dump(result, default_flow_style=False, sort_keys=False) )
    # print()

#------------------------------------------------------------------------------

if __name__ == "__main__":
    main()

#------------------------------------------------------------------------------
