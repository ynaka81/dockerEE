import unittest
import sys
sys.path.append("../../")
from dockerEE.element import *
from dockerEE.core import ContainerManagerImpl
from docker_container_test_utils import DockerContainerTestUtils

## TestServer
#
# The test case for Server
class TestServer(unittest.TestCase):
    ## init test case
    def setUp(self):
        host = "localhost"
        user = "vagrant"
        password = "vagrant"
        ## container manager
        self.__manager = ContainerManagerImpl(host, user, password)
        ## test utils
        self.__utils = DockerContainerTestUtils(host, user, password)
    ## test Server.__init__(self, manager, name)
    def testInit(self):
        server = "s1"
        s1 = Server(self.__manager, server)
        self.assertTrue(self.__utils.checkContainerExist(server))
    ## test Server.__del__(self)
    def testDel(self):
        servers = ["c1", "c2"]
        s = [Server(self.__manager, _s) for _s in servers]
        self.assertTrue(self.__utils.checkContainerExist(servers))
        del s[:]
        self.assertFalse(self.__utils.checkContainerExist(servers))
    ## test Server.command(command)
    def testCommand(self):
        server = "s1"
        s1 = Server(self.__manager, server)
        ret = s1.command("uname -n")
        self.assertEqual(ret.stdout, server)

if __name__ == "__main__":
    unittest.main()
