import unittest
import sys
sys.path.append("../../")
from dockerEE.remote import RemoteInterfaceImpl
from dockerEE.core import ContainerManagerImpl
from docker_container_test_utils import DockerContainerTestUtils

## TestContainer
#
# The test case for Container
class TestContainer(unittest.TestCase):
    ## init test case
    def setUp(self):
        host = "localhost"
        user = "vagrant"
        password = "vagrant"
        ## container_manager
        self.__manager = ContainerManagerImpl(host, user, password)
        ## test utils
        self.__utils = DockerContainerTestUtils(host, user, password)
    ## test Container.__del__(self)
    def testDel(self):
        container = "c1"
        c1 = self.__manager.create(container)
        del c1
        self.assertFalse(self.__utils.checkContainerExist(container))

## TestContainerManagerInmpl
#
# The test case for ContainerManagerImpl
class TestContainerManagerImpl(unittest.TestCase):
    ## init test case
    def setUp(self):
        host = "localhost"
        user = "vagrant"
        password = "vagrant"
        ## remote interface
        self.__interface = RemoteInterfaceImpl(host, user, password)
        ## container_manager
        self.__manager = ContainerManagerImpl("localhost", "vagrant", "vagrant")
        ## test utils
        self.__utils = DockerContainerTestUtils(host, user, password)
    ## test ContainerManagerImpl.createContainer(name)
    # @param self The object pointer
    def testCreateContainer(self):
        container = "c1"
        self.__manager.createContainer(container)
        self.assertTrue(self.__utils.checkContainerExist(container))
        self.__manager.destroyContainer(container)
    ## test ContainerManagerImpl.createContainer(name. privilege)
    # @param self The object pointer
    def testCreateContainerPrivilege(self):
        container = "c1"
        self.__manager.createContainer(container, privilege=["NET_ADMIN", "SYS_ADMIN"])
        ret = self.__interface.sudo("docker exec -it " + container + " umount /etc/hosts")
        self.assertEqual(ret.rc, 0)
        self.__manager.destroyContainer(container)
    ## test ContainerManagerImpl.createContainer(name, hosts)
    # @param self The object pointer
    def testCreateContainerHosts(self):
        container = "c1"
        hosts = [{"name": "c1", "IP": "1.0.1.10"}, {"name": "c2", "IP": "1.0.1.11"}]
        self.__manager.createContainer(container, hosts=hosts)
        ret = self.__interface.sudo("docker exec -it " + container + " cat /etc/hosts")
        container_hosts = ret.stdout.splitlines()[-len(hosts) - 1::2]
        for i in range(len(hosts)):
            host = hosts[i]
            container_host = container_hosts[i].split()
            self.assertEqual(host["name"], container_host[1])
            self.assertEqual(host["IP"], container_host[0])
        self.__manager.destroyContainer(container)
    ## test ContainerManagerImpl.createContainer(name, image)
    # @param self The object pointer
    def testCreateContainerImage(self):
        container = "c1"
        image = "centos:6"
        self.__manager.createContainer(container, image=image)
        ret = self.__interface.sudo("docker ps -a")
        lines = ret.stdout.splitlines()
        self.assertIn(image, lines[1].split())
        self.__manager.destroyContainer(container)
    ## test ContainerManagerImpl.__del__(self)
    # @param self The object pointer
    def testDel(self):
        container = "c1"
        self.__manager.createContainer(container)
        del self.__manager
        self.assertFalse(self.__utils.checkContainerExist(container))
    ## test ContainerManagerImpl.create(name)
    def testCreate(self):
        container = "c1"
        c1 = self.__manager.create(container)
        self.assertTrue(self.__utils.checkContainerExist(container))
    ## test ContainerManagerImpl.create(name, image)
    # @param self The object pointer
    def testCreateImage(self):
        container = "c1"
        image = "centos:6"
        c1 = self.__manager.create(container, image=image)
        ret = self.__interface.sudo("docker ps -a")
        lines = ret.stdout.splitlines()
        self.assertIn(image, lines[1].split())

    ## test ContainerManagerImpl.__init__(host, user, password) fail because of docker service not running
    # @param self The object pointer
    def testFailInit(self):
        self.__interface.sudo("service docker stop")
        with self.assertRaises(RuntimeError):
            self.setUp()
        self.__interface.sudo("service docker start")
    ## test ContainerManagerImpl.crete(name) fail because of same name instance
    # @param self The object pointer
    def testFailCreateContainerSameName(self):
        container = "c1"
        self.__manager.createContainer(container)
        with self.assertRaises(ValueError):
            self.__manager.createContainer(container)
        self.__manager.destroyContainer(container)
    ## test ContainerManagerImpl.createContainer(name) fail because docker service is not normally running
    # @param self The object pointer
    def testFailCreateContainerDockerNotRunning(self):
        self.__interface.sudo("service docker stop")
        with self.assertRaises(RuntimeError):
            self.__manager.createContainer("c1")
        self.__interface.sudo("service docker start")
    ## test ContainerManagerImpl.destroyContainer(name) fail because of not running the name container
    # @param self The object pointer
    def testFailDestroyContainerNotRunningContainer(self):
        with self.assertRaises(ValueError):
            self.__manager.destroyContainer("c1")
    ## test ContainerManagerImpl.destroyContainer(name) fail because docker service is not normally running
    # @param self The object pointer
    def testFailDestroyContainerDockerNotRunning(self):
        container = "c1"
        self.__manager.createContainer(container)
        self.__interface.sudo("service docker stop")
        with self.assertRaises(RuntimeError):
            self.__manager.destroyContainer(container)
        self.__interface.sudo("service docker start")
        self.__manager.destroyContainer(container)

if __name__ == "__main__":
    unittest.main()
