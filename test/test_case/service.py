import sys
sys.path.append("../../")

import unittest
import re

from dockerEE.remote import RemoteInterfaceImpl

from service_test_utils import ServiceTestUtils
from docker_container_test_utils import DockerContainerTestUtils

## TestEnvironmentEmulationServer
#
# The test case for EnvironmentEmulationService
class TestEnvironmentEmulationService(unittest.TestCase):
    ## init test case
    # @param self The object pointer
    def setUp(self):
        arg = {"host": "localhost", "user": "vagrant", "password": "vagrant"}
        stub = "/tmp/service_stub.py"
        ## service interface
        self.__service = ServiceTestUtils("python " + stub, **arg)
        ## remote interface
        self.__interface = RemoteInterfaceImpl(**arg)
        ## env.yml parameter
        self.__parameter = {"servers":[{"name": "s1", "image": "local/centos", "IPs": [{"dev": "eth0", "IP": "192.168.0.1/24", "gw": "192.168.0.254/24"}]}, {"name": "s2", "image": "local/centos", "IPs": [{"dev": "eth0", "IP": "192.168.0.2/24"}, {"dev": "eth1", "IP": "192.168.1.2/24", "gw": "192.168.1.254/24"}]}]}
        ## test utils
        self.__utils = DockerContainerTestUtils(**arg)
        ## environment definition file
        self.__filename = "/tmp/env.yml"
        # make service stub script
        f = open(stub, "w")
        f.write("import sys\n")
        f.write("sys.path.append('/vagrant')\n")
        f.write("from dockerEE.service import EnvironmentEmulationService\n")
        f.write("service = EnvironmentEmulationService('localhost', 'vagrant', 'vagrant')\n")
        f.write("service.action()")
        f.close()
        # make env.yml
        f = open(self.__filename, "w")
        f.write("---\n")
        f.write("servers:\n")
        for p in self.__parameter["servers"]:
            f.write("        - name: " + p["name"] + "\n")
            f.write("          image: " + p["image"] + "\n")
            f.write("          IPs:\n")
            for n in p["IPs"]:
                f.write("                  - dev: " + n["dev"] + "\n")
                f.write("                    IP: " + n["IP"] + "\n")
                if "gw" in n:
                    f.write("                    gw: " + n["gw"] + "\n")
        f.close()
    ## test "python service.py start/stop"
    # @param self The object pointer
    def testStartStop(self):
        servers = [x["name"] for x in self.__parameter["servers"]]
        ret = self.__service.start(self.__filename, 10)
        self.assertTrue(self.__utils.checkContainerExist(servers))
        for p in self.__parameter["servers"]:
            for n in p["IPs"]:
                ret = self.__interface.sudo("docker exec -it " + p["name"] + " ip addr show")
                self.assertTrue(re.search(r"inet " + n["IP"] + ".*" + n["dev"], ret.stdout))
                if "gw" in n:
                    ret = self.__interface.sudo("docker exec -it " + p["name"] + " ip route show")
                    self.assertIn("default via " + n["gw"].split("/")[0] + " dev " + n["dev"], ret.stdout)
        self.__service.stop(10)
        self.assertTrue(self.__utils.checkContainerNotExist(servers))
    ## test "python service.py status"
    # @param self The object pointer
    def testStatus(self):
        servers = [x["name"] for x in self.__parameter["servers"]]
        self.__service.start(self.__filename, 10)
        ret = self.__service.status()
        status =  "servers\n"
        for p in self.__parameter["servers"]:
            status += "\t" + p["name"] + "\n"
            for n in p["IPs"]:
                status += "\t\t" + n["dev"] + " : " + n["IP"]
                if "gw" in n:
                    status += " via " + n["gw"] + "\n"
                else:
                    status += "\n"
        ret.stdout += "\n"
        self.assertIn(status, ret.stdout)
        self.__service.stop(10)
        ret = self.__service.status()
        self.assertEqual(ret.rc, 0)
    ## test "python service.py reload"
    # @param self The object pointer
    def testReload(self):
        servers = [x["name"] for x in self.__parameter["servers"]]
        self.__service.start(self.__filename, 10)
        for s in servers:
            self.__interface.sudo("docker exec -it " + s + " touch /tmp/hello_dockerEE")
        for s in servers:
            ret = self.__interface.sudo("docker exec -it " + s + " test -f /tmp/hello_dockerEE", True)
            self.assertEqual(ret.rc, 0)
        self.__service.reload(servers[1:])
        ret = self.__interface.sudo("docker exec -it " + servers[0] + " test -f /tmp/hello_dockerEE", True)
        self.assertEqual(ret.rc, 0)
        ret = self.__interface.sudo("docker exec -it " + servers[1] + " test -f /tmp/hello_dockerEE", True)
        self.assertEqual(ret.rc, 1)
        for p in self.__parameter["servers"]:
            for n in p["IPs"]:
                ret = self.__interface.sudo("docker exec -it " + p["name"] + " ip addr show")
                self.assertTrue(re.search(r"inet " + n["IP"] + ".*" + n["dev"], ret.stdout))
                if "gw" in n:
                    ret = self.__interface.sudo("docker exec -it " + p["name"] + " ip route show")
                    self.assertIn("default via " + n["gw"].split("/")[0] + " dev " + n["dev"], ret.stdout)
        self.__service.stop(10)

if __name__ == "__main__":
    unittest.main()
