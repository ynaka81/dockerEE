import unittest
import sys
sys.path.append("../../")
import time
from service_test_utils import ServiceTestUtils
from dockerEE.remote import RemoteInterfaceImpl
from docker_container_test_utils import DockerContainerTestUtils

## TestEnvironmentEmulationServer
#
# The test case for EnvironmentEmulationService
class TestEnvironmentEmulationService(unittest.TestCase):
    ## execute stub
    # @param self The object pointer
    # @param action The action
    # @return CommandResult
    def __execStub(self, action):
        return self.__service_interface.sudo("python " + self.__stub + " " + action, True)
    ## init test case
    # @param self The object pointer
    def setUp(self):
        host = "localhost"
        user = "vagrant"
        password = "vagrant"
        ## stub file
        self.__stub = "/tmp/service_stub.py"
        ## service interface
        self.__service = ServiceTestUtils("python " + self.__stub, host, user, password)
        ## remote interface
        self.__interface = RemoteInterfaceImpl(host, user, password)
        ## env.yml parameter
        self.__parameter = {"servers":[{"name": "c1", "image": "centos"}, {"name": "c2", "image": "centos"}]}
        ## test utils
        self.__utils = DockerContainerTestUtils(host, user, password)
        ## environment definition file
        self.__filename = "/tmp/env.yml"
        # make stub script
        f = open(self.__stub, "w")
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
            f.write("- name: " + p["name"] + "\n")
            f.write("  image: " + p["image"] + "\n")
        f.close()
    ## test "python service.py start/stop"
    # @param self The object pointer
    def testStartStop(self):
        servers = [x["name"] for x in self.__parameter["servers"]]
        ret = self.__service.start(self.__filename)
        time.sleep(10)
        self.assertTrue(self.__utils.checkContainerExist(servers))
        self.__service.stop()
        time.sleep(10)
        self.assertTrue(self.__utils.checkContainerNotExist(servers))
    ## test "python service.py status"
    # @param self The object pointer
    def testStatus(self):
        servers = [x["name"] for x in self.__parameter["servers"]]
        self.__service.start(self.__filename)
        time.sleep(10)
        ret = self.__service.status()
        status =  "servers\n"
        status += "\tc2\n"
        status += "\tc1"
        self.assertIn(status, ret.stdout)
        self.__service.stop()
        time.sleep(10)
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
        self.__service.stop(10)

if __name__ == "__main__":
    unittest.main()
