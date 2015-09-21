import unittest
import sys
sys.path.append("../../")
import time
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
        return self.__interface.sudo("python " + self.__stub + " " + action, True)
    ## init test case
    # @param self The object pointer
    def setUp(self):
        host = "localhost"
        user = "vagrant"
        password = "vagrant"
        ## remote interface
        self.__interface = RemoteInterfaceImpl(host, user, password, pty=False)
        ## stub file
        self.__stub = "/tmp/service_stub.py"
        ## env.yml parameter
        self.__parameter = {"servers":[{"name": "c1", "image": "centos"}, {"name": "c2", "image": "centos"}]}
        ## test utils
        self.__utils = DockerContainerTestUtils(host, user, password)
        # make stub script
        f = open(self.__stub, "w")
        f.write("import sys\n")
        f.write("sys.path.append('/vagrant')\n")
        f.write("from dockerEE.service import EnvironmentEmulationService\n")
        f.write("service = EnvironmentEmulationService('localhost', 'vagrant', 'vagrant')\n")
        f.write("service.action()")
        f.close()
        # make env.yml
        yaml_file = "/tmp/env.yml"
        f = open(yaml_file, "w")
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
        ret = self.__execStub("start /tmp/env.yml")
        time.sleep(10)
        self.assertTrue(self.__utils.checkContainerExist(servers))
        ret = self.__execStub("stop")
        time.sleep(10)
        for s in servers:
            self.assertFalse(self.__utils.checkContainerExist(s))

if __name__ == "__main__":
    unittest.main()
