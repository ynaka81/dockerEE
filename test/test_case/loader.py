import sys
sys.path.append("../../")

import unittest
import re

from dockerEE.core import ContainerManagerImpl
from dockerEE.host import HostManagerImpl
from dockerEE.loader import *

from docker_container_test_utils import DockerContainerTestUtils

## TestServerLoader
#
# The test case for ServerLoader
class TestServerLoader(unittest.TestCase):
    ## init test case
    # @param self The object pointer
    def setUp(self):
        arg = {"host": "localhost", "user": "vagrant", "password": "vagrant"}
        ## container manager
        self.__container_manager = ContainerManagerImpl(**arg)
        ## host manager
        self.__host_manager = HostManagerImpl(**arg)
        ## test utils
        self.__utils = DockerContainerTestUtils(**arg)
    ## test ServerLoader.__call__(self.__manager, parameter)
    # @param self The object pointer
    def testCall(self):
        parameter = [{"name": "s1", "image": "local/centos"}, {"name": "s2", "image": "local/centos"}]
        servers = ServerLoader()(self.__container_manager, self.__host_manager, parameter)
        for p in parameter:
            self.assertIn(p["name"], servers)
            ret = servers[p["name"]].command("uname -n")
            self.assertEqual(ret.stdout, p["name"])
    ## test ServerLoader.__call__(self.__manager, parameter) with IPs
    # @param self The object pointer
    def testCallWithIPs(self):
        parameter = [{"name": "s1", "image": "local/centos", "IPs": [{"dev": "eth0", "IP": "192.168.0.1", "gw": "192.168.0.254"}]}, {"name": "s2", "image": "local/centos", "IPs": [{"dev": "eth0", "IP": "192.168.0.2"}, {"dev": "eth1", "IP": "192.168.1.2", "gw": "192.168.1.254"}]}]
        servers = ServerLoader()(self.__container_manager, self.__host_manager, parameter)
        for p in parameter:
            self.assertIn(p["name"], servers)
            server = servers[p["name"]]
            ret = server.command("ip addr show")
            for n in p["IPs"]:
                self.assertTrue(re.search(r"inet " + n["IP"] + ".*" + n["dev"], ret.stdout))
            ret = server.command("ip route show")
            for n in p["IPs"]:
                if "gw" in n:
                    self.assertIn("default via " + n["gw"] + " dev " + n["dev"], ret.stdout)

if __name__ == "__main__":
    unittest.main()
