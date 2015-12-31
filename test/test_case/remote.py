import sys
sys.path.append("../../")

import unittest

from dockerEE.remote import RemoteInterfaceImpl

## TestRemoteInterfaceInmpl
#
# The test case for RemoteInterfaceImpl
class TestRemoteInterfaceInmpl(unittest.TestCase):
    ## init test case
    def setUp(self):
        arg = {"host": "localhost", "user": "vagrant", "password": "vagrant"}
        ## remote_interface
        self.__interface = RemoteInterfaceImpl(**arg)
    ## test RemoteInterfaceImpl.sudo(command)
    # @param self The object pointer
    def testSudo(self):
        word = "HelloWold!"
        command = "echo " + word
        ret = self.__interface.sudo(command)
        self.assertEqual(ret.command, command)
        self.assertEqual(ret.rc, 0)
        self.assertEqual(ret.stdout, word)
        self.assertEqual(ret.stderr, "")
    ## test RemoteInterfaceImpl.sudo(command, True)
    # @param self The object pointer
    def testSudoIgnoreError(self):
        command = "cat hoge"
        ret = self.__interface.sudo(command, True)
        self.assertEqual(ret.command, command)
        self.assertEqual(ret.rc, 1)

if __name__ == "__main__":
    unittest.main()
