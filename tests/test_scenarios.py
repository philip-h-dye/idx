import sys

from io import StringIO

import json

import unittest

from parameterized import parameterized

from unittest.mock import patch

import idx

#------------------------------------------------------------------------------

class Test_Case ( unittest.TestCase ) :
        
    data_1 = "uid=197697(phdye) gid=197121(None) groups=197697(phdye),197121(None)"

    @parameterized.expand([
        [ "no_args", data_1, [], '\n'+data_1+'\n' ],
        #
        [ "list", data_1, ['--list'], """
uid=
197697(phdye)
gid=
197121(None)
groups=
197697(phdye)
197121(None)
"""
        ],
        #
        [ "yaml", data_1, ['--yaml'], """
user:
  uid: 197697
  gecos: phdye
group:
  gid: 197121
  gecos: None
groups:
- gid: 197697
  gecos: phdye
- gid: 197121
  gecos: None

"""
        ],
        #
        [ "json", data_1, ['--json'], """
{
  "user": {
    "uid": 197697,
    "gecos": "phdye"
  },
  "group": {
    "gid": 197121,
    "gecos": "None"
  },
  "groups": [
    { "gid": 197697,
      "gecos": "phdye"
    },
    { "gid": 197121,
      "gecos": "None"
    }
  ]
}
"""
        ],
        #
        [ "groups", "197697 197121", ['--groups'], "\n197697 197121\n" ],
        #
        [ "groups-list", "197697 197121", ['--groups', '--list'], "\n197697\n197121\n" ],
        #
        [ "groups-yaml", "197697 197121", ['--groups', '--yaml'], """
groups:
- gid: 197697
- gid: 197121

"""
        ],
        #
        [ "groups-json", "197697 197121", ['--groups', '--json'], """
{
  "groups": [
    { "gid": 197697
    },
    { "gid": 197121
    }
  ]
}
"""
        ],
        #
    ] )

    def test_idx ( self, test_name, data, options, expected ):

        with patch('sys.stdout', new = StringIO()) as mock_out :
            idx.main(['id', '--data', data]+options)

        result = '\n' + mock_out.getvalue()

        with open(f'log/out/{test_name}/result', 'w') as r, open('expected', 'w') as e :
            r.write( result )

        with open(f'log/out/{test_name}/expected', 'w') as e:
            e.write( expected )

        self.assertEqual ( result, expected )

#------------------------------------------------------------------------------
