import sys
sys.path.append("../../")

import unittest
import re
from ipaddress import ip_interface

from dockerEE.remote import RemoteInterfaceImpl
from dockerEE.core import ContainerManagerImpl
from dockerEE.host import HostManagerImpl
from dockerEE.element import *

from docker_container_test_utils import DockerContainerTestUtils

## TestServer
#
# The test case for Server
class TestServer(unittest.TestCase):
    ## init test case
    # @param self The object pointer
    def setUp(self):
        arg = {"host": "localhost", "user": "vagrant", "password": "vagrant"}
        ## remote interface
        self.__interface = RemoteInterfaceImpl(**arg)
        ## container manager
        self.__container_manager = ContainerManagerImpl(**arg)
        ## host OS manager
        self.__host_manager = HostManagerImpl(**arg)
        ## test utils
        self.__utils = DockerContainerTestUtils(**arg)
    ## test Server.__init__(self, container_manager, name)
    # @param self The object pointer
    def testInit(self):
        server = "s1"
        s1 = Server(self.__container_manager, server)
        self.assertTrue(self.__utils.checkContainerExist(server))
    ## test Server.__del__(self)
    # @param self The object pointer
    def testDel(self):
        servers = ["s1", "s2"]
        s = [Server(self.__container_manager, _s) for _s in servers]
        self.assertTrue(self.__utils.checkContainerExist(servers))
        del s[:]
        self.assertFalse(self.__utils.checkContainerExist(servers))
    ## test Server.__del__(self) with IP
    # @param self The object pointer
    def testDestroyIP(self):
        server_info = [{"name": "s1", "ip": ip_interface(u"192.168.0.1/24")}, {"name": "s2", "ip": ip_interface(u"192.168.0.2/24")}]
        servers = []
        for s in server_info:
            servers.append(Server(self.__container_manager, s["name"]))
            servers[-1].attachIP(self.__host_manager, "eth0", s["ip"])
        self.assertTrue(self.__utils.checkContainerExist([s["name"] for s in server_info]))
        self.assertIn("br_192.168.0.0", self.__interface.sudo("ip addr show").stdout)
        del servers[0]
        self.assertIn("br_192.168.0.0", self.__interface.sudo("ip addr show").stdout)
        del servers[0]
        self.assertNotIn("br_192.168.0.0", self.__interface.sudo("ip addr show").stdout)
    ## test Server.getNetworkInfo(self)
    # @param self The object pointer
    def testGetNetworkInfo(self):
        network = [{"dev": "eth0", "IP": ip_interface(u"192.168.0.1/24"), "gw": None}, {"dev": "eth1", "IP": ip_interface(u"192.168.1.2/24"), "gw": ip_interface(u"192.168.1.254/24")}]
        s1 = Server(self.__container_manager, "s1")
        for n in network:
            if n["gw"] is not None:
                s1.attachIP(self.__host_manager, n["dev"], n["IP"], n["gw"])
            else:
                s1.attachIP(self.__host_manager, n["dev"], n["IP"])
        self.assertEqual(s1.getNetworkInfo(), network)
    ## test Server.command(command)
    # @param self The object pointer
    def testCommand(self):
        server = "s1"
        s1 = Server(self.__container_manager, server)
        ret = s1.command("uname -n")
        self.assertEqual(s1.command("uname -n").stdout, server)
    ## test Server.attachIP(host_manager, dev, IP, gw)
    # @param self The object pointer
    def testAttachIP(self):
        network = [{"dev": "eth0", "IP": ip_interface(u"192.168.0.1/24"), "gw": None}, {"dev": "eth1", "IP": ip_interface(u"192.168.1.2/24"), "gw": ip_interface(u"192.168.1.254/24")}]
        s1 = Server(self.__container_manager, "s1")
        for n in network:
            if n["gw"] is not None:
                s1.attachIP(self.__host_manager, n["dev"], n["IP"], n["gw"])
            else:
                s1.attachIP(self.__host_manager, n["dev"], n["IP"])
        ret = s1.command("ip addr show")
        for n in network:
            self.assertTrue(re.search(r"inet " + str(n["IP"]) + ".*" + n["dev"], ret.stdout))
        ret = s1.command("ip route show")
        for n in network:
            if n["gw"] is not None:
                self.assertIn("default via " + str(n["gw"].ip) + " dev " + n["dev"], ret.stdout)
    ## test Server.reload(self)
    # @param self The object pointer
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
    # @param self The object pointer
    def testReloadOptions(self):
        image = "centos:6"
        s1 = Server(self.__container_manager, "s1", source=image)
        s1.reload(self.__container_manager, self.__host_manager)
        self.assertIn(image, self.__interface.sudo("docker ps -a").stdout.splitlines()[1].split())
    ## test Server.reload(self) with IP
    # @param self The object pointer
    def testReloadIP(self):
        network = [{"dev": "eth0", "IP": ip_interface(u"192.168.0.1/24"), "gw": None}, {"dev": "eth1", "IP": ip_interface(u"192.168.1.2/24"), "gw": ip_interface(u"192.168.1.254/24")}]
        s1 = Server(self.__container_manager, "s1")
        for n in network:
            if n["gw"] is not None:
                s1.attachIP(self.__host_manager, n["dev"], n["IP"], n["gw"])
            else:
                s1.attachIP(self.__host_manager, n["dev"], n["IP"])
        s1.reload(self.__container_manager, self.__host_manager)
        ret = s1.command("ip addr show")
        for n in network:
            self.assertTrue(re.search(r"inet " + str(n["IP"]) + ".*" + n["dev"], ret.stdout))
        ret = s1.command("ip route show")
        for n in network:
            if n["gw"] is not None:
                self.assertIn("default via " + str(n["gw"].ip) + " dev " + n["dev"], ret.stdout)

if __name__ == "__main__":
    unittest.main()
