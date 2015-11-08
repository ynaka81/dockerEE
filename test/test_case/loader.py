import unittest
import sys
sys.path.append("../../")
import re
from dockerEE.loader import *
from dockerEE.core import ContainerManagerImpl
from dockerEE.host import HostManagerImpl
from docker_container_test_utils import DockerContainerTestUtils

## TestServerLoader
#
# The test case for ServerLoader
class TestServerLoader(unittest.TestCase):
    ## init test case
    def setUp(self):
        host = "localhost"
        user = "vagrant"
        password = "vagrant"
        ## container manager
        self.__container_manager = ContainerManagerImpl(host, user, password)
        ## host manager
        self.__host_manager = HostManagerImpl(host, user, password)
        ## test utils
        self.__utils = DockerContainerTestUtils(host, user, password)
    ## test ServerLoader.__call__(self.__manager, parameter)
    def testCall(self):
        parameter = [{"name": "c1", "image": "centos"}, {"name": "c2", "image": "centos"}]
        servers = ServerLoader()(self.__container_manager, self.__host_manager, parameter)
        for p in parameter:
            self.assertTrue(p["name"] in servers)
            ret = servers[p["name"]].command("uname -n")
            self.assertEqual(ret.stdout, p["name"])
    ## test ServerLoader.__call__(self.__manager, parameter) with IPs
    def testCallWithIPs(self):
        parameter = [{"name": "c1", "image": "centos", "IPs": [{"dev": "eth0", "IP": "192.168.0.1", "gw": "192.168.0.254"}]}, {"name": "c2", "image": "centos", "IPs": [{"dev": "eth0", "IP": "192.168.0.2"}, {"dev": "eth1", "IP": "192.168.1.2", "gw": "192.168.1.254"}]}]
        servers = ServerLoader()(self.__container_manager, self.__host_manager, parameter)
        for p in parameter:
            self.assertTrue(p["name"] in servers)
            server = servers[p["name"]]
            ret = servers[p["name"]].command("uname -n")
            self.assertEqual(ret.stdout, p["name"])
            for n in p["IPs"]:
                ret = server.command("ip addr show")
                self.assertTrue(re.search(r"inet " + n["IP"] + ".*" + n["dev"], ret.stdout))
                if "gw" in n:
                    ret = server.command("ip route show")
                    self.assertIn("default via " + n["gw"] + " dev " + n["dev"], ret.stdout)

if __name__ == "__main__":
    unittest.main()
