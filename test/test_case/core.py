import unittest
import sys
from ipaddress import ip_interface
import re
sys.path.append("/vagrant/dockerEE/remote")
from remote_interface import CommandResult
sys.path.append("/vagrant/dockerEE/core")
from container_manager import ContainerManager
sys.path.append("../../")
from dockerEE.remote import RemoteInterfaceImpl
from dockerEE.core import ContainerManagerImpl
from docker_container_test_utils import DockerContainerTestUtils

## ContainerManagerStub
#
# The stub class to control container
class ContainerManagerStub(ContainerManager):
    ## constructor
    def __init__(self):
        ## the container list
        self.__container = []
    ## stub method of creating container
    # @param self The object pointer
    # @param container The container that will be created
    # @param options The options to create container
    def createContainerImpl(self, container, **options):
        self.__container.append({"name": container.getName(), "options": options})
    ## stub method of destroying container
    # @param self The object pointer
    # @param container The container that will be created
    def destroyContainerImpl(self, container):
        self.__container[:] = [c for c in self.__container if not c["name"] == container.getName()]
    ## stub method of executing command on container
    # @param self The object pointer
    # @param container The container that will be created
    # @param command The command to execute on container
    # @return CommandResult
    def command(self, container, command):
        return CommandResult(command, 0, "stdout", "stderr")
    ## stub method of attaching IP to container
    # @param self The object pointer
    # @param container The container that will be created
    # @param segment The name of the segment which the IP is attached on
    # @param dev The device name of container
    # @param IP The IP attached to the container
    # @param gw The gateway address if the device is default gateway
    def attachIP(self, container, segment, dev, IP, gw):
        c = (c for c in self.__container if c["name"] == container.getName()).next()
        c["segment"] = segment
        c["dev"] = dev
        c["IP"] = IP
        c["gw"] = gw
    ## get the container list
    # @param self The object pointer
    # @return the container list
    def get(self):
        return self.__container

## TestContainerManager
#
# The test case for ContainerManager
class TestContainerManager(unittest.TestCase):
    ## init test case
    def setUp(self):
        ## container_manager
        self.__manager = ContainerManagerStub()
    ## test ContainerManager.create(name)
    # @param self The object pointer
    def testCreate(self):
        container1 = "c1"
        container2 = "c2"
        c1 = self.__manager.create(container1)
        c2 = self.__manager.create(container2)
        self.assertEqual(self.__manager.get(), [{"name": container1, "options": {}}, {"name": container2, "options": {}}])
    ## test ContainerManager.create(name, options)
    # @param self The object pointer
    def testCreateWithOptions(self):
        container = {"name": "c", "options": {"option1": 10, "option2": "test"}}
        c = self.__manager.create(container["name"], **container["options"])
        self.assertEqual(self.__manager.get(), [container])

    ## test ContainerManager.create(name) fails because of the container already exists
    # @param self The object pointer
    def testFailCreate(self):
        container = "c"
        c1 = self.__manager.create(container)
        with self.assertRaises(ValueError):
            c2 = self.__manager.create(container)

## TestContainer
#
# The test case for Container
class TestContainer(unittest.TestCase):
    ## init test case
    def setUp(self):
        ## container_manager
        self.__manager = ContainerManagerStub()
    ## test Container.__del__(self)
    def testDel(self):
        container = "c"
        c = self.__manager.create(container)
        self.assertIn(container, [_c["name"] for _c in self.__manager.get()])
        del c
        self.assertNotIn(container, [_c["name"] for _c in self.__manager.get()])
    ## test Container.destroy(self):
    # @param self The object pointer
    def testDestroy(self):
        container = "c"
        c = self.__manager.create(container)
        self.assertIn(container, [_c["name"] for _c in self.__manager.get()])
        c.destroy()
        self.assertNotIn(container, [_c["name"] for _c in self.__manager.get()])
    ## test Container.__checkDestroyed(self):
    # @param self The object pointer
    def testCheckDestroyed(self):
        container = "c"
        c = self.__manager.create(container)
        c.destroy()
        with self.assertRaises(RuntimeError):
            c.command("command")
    ## test Container.getName()
    # @param self The object pointer
    def testGetName(self):
        container = "c"
        c = self.__manager.create(container)
        self.assertEqual(c.getName(), container)
    ## test Container.getOptions()
    # @param self The object pointer
    def testGetOptions(self):
        container = "c"
        options = {"option1": 10, "option2": "test"}
        c = self.__manager.create(container, **options)
        self.assertEqual(c.getOptions(), options)
    ## test Container.command(command)
    # @param self The object pointer
    def testCommand(self):
        container = "c"
        c = self.__manager.create(container)
        ret = c.command("command")
        cr = CommandResult("command", 0, "stdout", "stderr")
        self.assertEqual(ret.command, cr.command)
        self.assertEqual(ret.rc, cr.rc)
        self.assertEqual(ret.stdout, cr.stdout)
        self.assertEqual(ret.stderr, cr.stderr)
    ## test Container.attachIP(segment, dev, IP)
    # @param self The object pointer
    def testAttachIP(self):
        container = "c"
        c = self.__manager.create(container)
        bridge = "br1"
        ip = ip_interface(u"192.168.0.1/24")
        dev = "eth0"
        c.attachIP(bridge, dev, ip)
        self.assertEqual(self.__manager.get(), [{"name": container, "options": {}, "segment": bridge, "dev": dev, "IP": ip, "gw": None}])
    ## test Container.attachIP(segment, dev, IP, gw)
    # @param self The object pointer
    def testAttachIPWithGW(self):
        container = "c"
        c = self.__manager.create(container)
        bridge = "br1"
        ip = ip_interface(u"192.168.0.1/24")
        dev = "eth0"
        gw = ip_interface(u"192.168.0.254/24")
        c.attachIP(bridge, dev, ip, gw)
        self.assertEqual(self.__manager.get(), [{"name": container, "options": {}, "segment": bridge, "dev": dev, "IP": ip, "gw": gw}])

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
        self.__manager = ContainerManagerImpl(host, user, password)
        ## test utils
        self.__utils = DockerContainerTestUtils(host, user, password)
    ## test ContainerManagerImpl.create(name)
    # @param self The object pointer
    def testCreate(self):
        container = "c1"
        c = self.__manager.create(container)
        self.assertTrue(self.__utils.checkContainerExist(container))
    ## test ContainerManagerImpl.create(name. privilege)
    # @param self The object pointer
    def testCreateWithPrivilege(self):
        container = "c1"
        c = self.__manager.create(container, privilege=["NET_ADMIN", "SYS_ADMIN"])
        ret = self.__interface.sudo("docker exec -it " + container + " umount /etc/hosts")
        self.assertEqual(ret.rc, 0)
    ## test ContainerManagerImpl.create(name, hosts)
    # @param self The object pointer
    def testCreateWithHosts(self):
        container = "c1"
        hosts = [{"name": "c1", "IP": "1.0.1.10"}, {"name": "c2", "IP": "1.0.1.11"}]
        c = self.__manager.create(container, hosts=hosts)
        ret = self.__interface.sudo("docker exec -it " + container + " cat /etc/hosts")
        container_hosts = ret.stdout.splitlines()[-len(hosts) - 1::2]
        for i in range(len(hosts)):
            host = hosts[i]
            container_host = container_hosts[i].split()
            self.assertEqual(host["name"], container_host[1])
            self.assertEqual(host["IP"], container_host[0])
    ## test ContainerManagerImpl.create(name, image)
    # @param self The object pointer
    def testCreateWithImage(self):
        container = "c1"
        image = "centos:6"
        c = self.__manager.create(container, image=image)
        ret = self.__interface.sudo("docker ps -a")
        lines = ret.stdout.splitlines()
        self.assertIn(image, lines[1].split())
    ## test ContainerManagerImpl.destroyContainerImpl(self, container)
    # @param self The object pointer
    def testDestroy(self):
        container = "c1"
        c = self.__manager.create(container)
        self.assertTrue(self.__utils.checkContainerExist(container))
        del c
        self.assertTrue(self.__utils.checkContainerNotExist(container))
    ## test ContainerManagerImpl.command(container, command)
    # @param self The object pointer
    def testCommand(self):
        container = "c1"
        c = self.__manager.create(container)
        ret = c.command("uname -n")
        self.assertEqual(ret.stdout, container)
    ## test ContainerManagerImpl.attachIP(container, segment, dev, IP, gw)
    # @param self The object pointer
    def testAttachIP(self):
        bridge = "br1"
        self.__interface.sudo("brctl addbr " + bridge)
        self.__interface.sudo("ip link set " + bridge + " up")
        container = "c1"
        c = self.__manager.create(container)
        ip1 = ip_interface(u"192.168.0.1/24")
        dev1 = "eth0"
        c.attachIP(bridge, dev1, ip1)
        ret = c.command("ip addr show")
        self.assertTrue(re.search(r"inet " + str(ip1) + ".*" + dev1, ret.stdout))
        ip2 = ip_interface(u"192.168.1.1/24")
        dev2 = "eth1"
        gw = ip_interface(u"192.168.1.254/24")
        c.attachIP(bridge, dev2, ip2, gw)
        ret = c.command("ip addr show")
        self.assertTrue(re.search(r"inet " + str(ip2) + ".*" + dev2, ret.stdout))
        ret = c.command("ip route show")
        self.assertIn("default via " + str(gw.ip) + " dev " + dev2, ret.stdout)
        self.__interface.sudo("ip link set " + bridge + " down")
        self.__interface.sudo("brctl delbr " + bridge)

    ## test ContainerManagerImpl.__init__(host, user, password) fail because of docker service not running
    # @param self The object pointer
    def testFailInit(self):
        self.__interface.sudo("service docker stop")
        with self.assertRaises(RuntimeError):
            self.setUp()
        self.__interface.sudo("service docker start")
    ## test ContainerManagerImpl.create(name) fail because docker service is not normally running
    # @param self The object pointer
    def testFailCreateContainerDockerNotRunning(self):
        self.__interface.sudo("service docker stop")
        with self.assertRaises(RuntimeError):
            self.__manager.create("c1")
        self.__interface.sudo("service docker start")
    ## test ContainerManagerImpl.destroyContainerImpl(container) fail because docker service is not normally running
    # @param self The object pointer
    def testFailDestroyContainerDockerNotRunning(self):
        container = "c1"
        c = self.__manager.create(container)
        self.__interface.sudo("service docker stop")
        with self.assertRaises(RuntimeError):
            c.destroy()
        self.__interface.sudo("service docker start")
    ## test ContainerManagerImpl.command(container, command) fail because the command does not exist
    # @param self The object pointer
    def testFailCommand(self):
        container = "c1"
        c = self.__manager.create(container)
        with self.assertRaises(RuntimeError):
            c.command("fail")
    ## test ContainerManagerImpl.attachIP(container, segment, dev, IP) fail bacause the same dev is already created
    # @param self The object pointer
    def testFailAttachIP(self):
        bridge = "br1"
        self.__interface.sudo("brctl addbr " + bridge)
        self.__interface.sudo("ip link set " + bridge + " up")
        container = "c1"
        c = self.__manager.create(container)
        ip = ip_interface(u"192.168.0.1/24")
        dev = "eth0"
        c.attachIP(bridge, dev, ip)
        with self.assertRaises(RuntimeError):
            c.attachIP(bridge, dev, ip)
        self.__interface.sudo("ip link set " + bridge + " down")
        self.__interface.sudo("brctl delbr " + bridge)

if __name__ == "__main__":
    unittest.main()
