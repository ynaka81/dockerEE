import unittest
import sys
sys.path.append("../../")
from dockerEE.element import *
from dockerEE.remote import RemoteInterfaceImpl
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
        ## remote interface
        self.__interface = RemoteInterfaceImpl(host, user, password)
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
    ## test Server.reload(self)
    def testReload(self):
        s1 = Server(self.__manager, "s1")
        ret = s1.command("touch /tmp/hello_dockerEE")
        self.assertEqual(ret.rc, 0)
        ret = s1.command("test -f /tmp/hello_dockerEE")
        self.assertEqual(ret.rc, 0)
        s1.reload(self.__manager)
        with self.assertRaises(RuntimeError):
            ret = s1.command("test -f /tmp/hello_dockerEE")
    ## test Server.reload(self, options)
    def testReloadOptions(self):
        image = "centos:6"
        s1 = Server(self.__manager, "s1", source=image)
        s1.reload(self.__manager)
        ret = self.__interface.sudo("docker ps -a")
        lines = ret.stdout.splitlines()
        self.assertIn(image, lines[1].split())

if __name__ == "__main__":
    unittest.main()
