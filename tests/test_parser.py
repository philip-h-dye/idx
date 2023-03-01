import unittest

import idx.parser

class Test_Parse ( unittest.TestCase ) :

    def setUp(self) :
        pass

    def test_basic(self) :

        input = "uid=197697(phdye) gid=197121(None) groups=197697(phdye),197121(None)"

        expect =  { "user"   : { 'uid' : 197697, 'gecos' : "phdye" },
                    "group"  : { 'gid' : 197121, 'gecos' : "None" },
                    "groups" : [ { 'gid' : 197697, 'gecos' : "phdye" },
                                 { 'gid' : 197121, 'gecos' : "None" } ] }

        self.assertEqual ( idx.parser.parse(input), expect )

    def test_long(self) :

        input = "uid=197697(phdye) gid=197121(None) groups=197121(None),197614(docker-users),197615(mlocate),545(Users),559(Performance Log Users),4(INTERACTIVE),66049(CONSOLE LOGON),11(AuthUser),15(This Organization),113(Local account),4095(CurrentSession),66048(LOCAL),262154(NTLM Authentication),401408(Medium Mandatory Level)"

        expect =  {'user': {'uid': 197697, 'gecos': 'phdye'},
                   'group': {'gid': 197121, 'gecos': 'None'},
                   'groups': [{'gid': 197121, 'gecos': 'None'},
                              {'gid': 197614, 'gecos': 'docker-users'},
                              {'gid': 197615, 'gecos': 'mlocate'},
                              {'gid': 545, 'gecos': 'Users'},
                              {'gid': 559, 'gecos': 'Performance Log Users'},
                              {'gid': 4, 'gecos': 'INTERACTIVE'},
                              {'gid': 66049, 'gecos': 'CONSOLE LOGON'},
                              {'gid': 11, 'gecos': 'AuthUser'},
                              {'gid': 15, 'gecos': 'This Organization'},
                              {'gid': 113, 'gecos': 'Local account'},
                              {'gid': 4095, 'gecos': 'CurrentSession'},
                              {'gid': 66048, 'gecos': 'LOCAL'},
                              {'gid': 262154, 'gecos': 'NTLM Authentication'},
                              {'gid': 401408, 'gecos': 'Medium Mandatory Level'}]}

        self.assertEqual ( idx.parser.parse(input), expect )
