#!/usr/bin/env python

import subprocess
import json
from pyparsing import Word, nums, Suppress, Group, alphas, Combine, OneOrMore
from pyparsing import printables, White, ZeroOrMore, Optional

def parse ( text ):

    # Define a grammar for parsing id output
    S = Suppress

    uid = Word(nums)('uid').setParseAction(lambda t: int(t[0]))
    gid = Word(nums)('gid').setParseAction(lambda t: int(t[0]))
    gecos = S('(') + Combine(OneOrMore(Word(printables, excludeChars=")") | White(' ')))("gecos") + S(')')

    user = Group(S('uid=') + uid + gecos)
    group_item = gid + gecos
    group = Group(S('gid=') + gid + gecos)
    groups = Group(Suppress('groups=') + ZeroOrMore(Group(group_item) + Optional(Suppress(','))))

    grammar = user('user') + group('group') + groups('groups')
    
    # Parse id output
    result = grammar.parseString(text)

    # Convert result to JSON format
    return {
        'user': {
            'uid': result.user.uid,
            'gecos': result.user.gecos
        },
        'group': {
            'gid': result.group.gid,
            'gecos': result.group.gecos
        },
        'groups': [
            {
                'gid': g.gid,
                'gecos': g.gecos
            } for g in result.groups
        ]
    }

#------------------------------------------------------------------------------

if __name__ == "__main__":

    text = "uid=197697(phdye) gid=197121(None) groups=197697(phdye),197121(None)"

    expect =  { "user"   : { 'uid' : 197697, 'gecos' : "phdye" },
                "group"  : { 'gid' : 197121, 'gecos' : "None" },
                "groups" : [ { 'gid' : 197697, 'gecos' : "phdye" },
                             { 'gid' : 197121, 'gecos' : "None" } ] }

    result = parse(text)

    # assert result == expect

    import json
    print("JSON:")
    print( json.dumps(result, indent=4) )
    print()

    import yaml
    print("YAML:")
    print( yaml.dump(result, default_flow_style=False, sort_keys=False) )
    print()

#------------------------------------------------------------------------------
