import unittest
import sys
import re
from ipaddress import ip_interface
sys.path.append("../../")
from dockerEE.element import *
from dockerEE.remote import RemoteInterfaceImpl
from dockerEE.core import ContainerManagerImpl
from dockerEE.host import HostManagerImpl
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
        self.__container_manager = ContainerManagerImpl(host, user, password)
        ## host OS manager
        self.__host_manager = HostManagerImpl(host, user, password)
        ## test utils
        self.__utils = DockerContainerTestUtils(host, user, password)
    ## test Server.__init__(self, container_manager, name)
    def testInit(self):
        server = "s1"
        s1 = Server(self.__container_manager, server)
        self.assertTrue(self.__utils.checkContainerExist(server))
    ## test Server.__del__(self)
    def testDel(self):
        servers = ["c1", "c2"]
        s = [Server(self.__container_manager, _s) for _s in servers]
        self.assertTrue(self.__utils.checkContainerExist(servers))
        del s[:]
        self.assertFalse(self.__utils.checkContainerExist(servers))
    ## test Server.command(command)
    def testCommand(self):
        server = "s1"
        s1 = Server(self.__container_manager, server)
        ret = s1.command("uname -n")
        self.assertEqual(ret.stdout, server)
    ## test Server.attachIP(host_manager, dev, IP, gw)
    # @param self The object pointer
    def testAttachIP(self):
        server1 = "s1"
        s1 = Server(self.__container_manager, server1)
        dev1 = "eth0"
        ip1 = ip_interface(u"192.168.0.1/24")
        s1.attachIP(self.__host_manager, dev1, ip1)
        dev2 = "eth1"
        ip2 = ip_interface(u"192.168.1.1/24")
        gw = ip_interface(u"192.168.1.254/24")
        s1.attachIP(self.__host_manager, dev2, ip2, gw)
        ret = s1.command("ip addr show")
        self.assertTrue(re.search(r"inet " + str(ip1) + ".*" + dev1, ret.stdout))
        ret = s1.command("ip addr show")
        self.assertTrue(re.search(r"inet " + str(ip2) + ".*" + dev2, ret.stdout))
        ret = s1.command("ip route show")
        self.assertIn("default via " + str(gw.ip) + " dev " + dev2, ret.stdout)
        server2 = "s2"
        s2 = Server(self.__container_manager, server2)
        dev3 = "eth0"
        ip3 = ip_interface(u"192.168.0.1/24")
        s2.attachIP(self.__host_manager, dev3, ip3)
        ret = s2.command("ip addr show")
        self.assertTrue(re.search(r"inet " + str(ip3) + ".*" + dev3, ret.stdout))
    ## test Server.reload(self)
    def testReload(self):
        s1 = Server(self.__container_manager, "s1")
        ret = s1.command("touch /tmp/hello_dockerEE")
        self.assertEqual(ret.rc, 0)
        ret = s1.command("test -f /tmp/hello_dockerEE")
        self.assertEqual(ret.rc, 0)
        s1.reload(self.__container_manager, self.__host_manager)
        with self.assertRaises(RuntimeError):
            ret = s1.command("test -f /tmp/hello_dockerEE")
    ## test Server.reload(self, options)
    def testReloadOptions(self):
        image = "centos:6"
        s1 = Server(self.__container_manager, "s1", source=image)
        s1.reload(self.__container_manager, self.__host_manager)
        ret = self.__interface.sudo("docker ps -a")
        lines = ret.stdout.splitlines()
        self.assertIn(image, lines[1].split())
    ## test Server.reload(self) with IP
    def testReloadIP(self):
        s1 = Server(self.__container_manager, "s1")
        dev1 = "eth0"
        ip1 = ip_interface(u"192.168.0.1/24")
        dev2 = "eth1"
        ip2 = ip_interface(u"192.168.1.1/24")
        gw = ip_interface(u"192.168.1.254/24")
        s1.attachIP(self.__host_manager, dev1, ip1)
        s1.attachIP(self.__host_manager, dev2, ip2, gw)
        s1.reload(self.__container_manager, self.__host_manager)
        ret = s1.command("ip addr show")
        self.assertTrue(re.search(r"inet " + str(ip1) + ".*" + dev1, ret.stdout))
        self.assertTrue(re.search(r"inet " + str(ip2) + ".*" + dev2, ret.stdout))
        ret = s1.command("ip route show")
        self.assertIn("default via " + str(gw.ip) + " dev " + dev2, ret.stdout)

if __name__ == "__main__":
    unittest.main()
