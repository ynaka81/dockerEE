import unittest
import sys
sys.path.append("../../")
from dockerEE.loader import *
from dockerEE.core import ContainerManagerImpl
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
        self.__manager = ContainerManagerImpl(host, user, password)
        ## test utils
        self.__utils = DockerContainerTestUtils(host, user, password)
    ## test ServerLoader.__call__(self.__manager, parameter)
    def testCall(self):
        parameter = [{"name": "c1", "image": "centos"}, {"name": "c2", "image": "centos"}]
        servers = ServerLoader()(self.__manager, parameter)
        for p in parameter:
            self.assertTrue(p["name"] in servers)

if __name__ == "__main__":
    unittest.main()
