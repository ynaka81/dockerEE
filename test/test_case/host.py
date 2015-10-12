import unittest
from ipaddress import ip_interface
import sys
sys.path.append("/vagrant/dockerEE/host")
from host_manager import HostManager
sys.path.append("../../")
from dockerEE.remote import RemoteInterfaceImpl
from dockerEE.host import HostManagerImpl

## HostManagerStub
#
# The stub class to control host OS
class HostManagerStub(HostManager):
    ## constructor
    def __init__(self):
        ## the list of network address
        self.__network = []
    ## stub method of creating bridge
    # @param self The object pointer
    # @param network_address The network address of the bridge
    def createBridgeImpl(self, network_address):
        self.__network.append(network_address)
    ## stub method of destroying container
    # @param self The object pointer
    # @param network_address The network address of the bridge
    def destroyBridgeImpl(self, network_address):
        self.__network.remove(network_address)
    ## get the list of network address
    # @param self The object pointer
    # @return the list of network address
    def get(self):
        return self.__network

## TestHostManager
#
# The test case for HostManager
class TestHostManager(unittest.TestCase):
    ## init test case
    def setUp(self):
        ## host OS manager
        self.__manager = HostManagerStub()
    ## test HostManager.createBridge(network_address)
    # @param self The object pointer
    def testCreateBridge(self):
        ip = ip_interface(u"192.168.33.10/24")
        b = self.__manager.createBridge(ip.network)
        self.assertEqual(self.__manager.get(), [ip.network])
        del b
        self.assertEqual(self.__manager.get(), [])
    ## test HostManager.createBridge(network_address) when the network_addresses is the same
    # @param self The object pointer
    def testCreateBridgeSameIPs(self):
        ip = ip_interface(u"192.168.33.10/24")
        b1 = self.__manager.createBridge(ip.network)
        b2 = self.__manager.createBridge(ip.network)
        self.assertEqual(self.__manager.get(), [ip.network])
        del b1
        self.assertEqual(self.__manager.get(), [ip.network])
        del b2
        self.assertEqual(self.__manager.get(), [])
    ## test HostManager.createBridge(network_address) when the network_addresses is the different
    # @param self The object pointer
    def testCreateBridgeDifferentIPs(self):
        ip1 = ip_interface(u"192.168.30.10/24")
        ip2 = ip_interface(u"192.168.33.10/24")
        b1 = self.__manager.createBridge(ip1.network)
        b2 = self.__manager.createBridge(ip2.network)
        self.assertEqual(self.__manager.get(), [ip1.network, ip2.network])
        del b1
        self.assertEqual(self.__manager.get(), [ip2.network])
        del b2
        self.assertEqual(self.__manager.get(), [])

## TestHostManagerImpl
#
# The test case for HostManagerImpl
class TestHostManagerImpl(unittest.TestCase):
    ## init test case
    def setUp(self):
        host = "localhost"
        user = "vagrant"
        password = "vagrant"
        ## remote interface
        self.__interface = RemoteInterfaceImpl(host, user, password)
        ## host OS manager
        self.__manager = HostManagerImpl(host, user, password)
    ## check if the bridge exists
    # @param self The object pointer
    # @param network_address The network address of the bridge
    def __checkBridgeExist(self, network):
        ret = self.__interface.sudo("ip addr show | grep br_" + str(network).split("/")[0], True)
        return ret.rc == 0
    ## test HostManager.createBridge(network_address)
    # @param self The object pointer
    def testCreateBridge(self):
        ip = ip_interface(u"192.168.33.10/24")
        b = self.__manager.createBridge(ip.network)
        self.assertTrue(self.__checkBridgeExist(ip.network))
        del b
        self.assertFalse(self.__checkBridgeExist(ip.network))

    ## test HostManager.createBridge(network_address) fail because the bridge already exists
    # @param self The object pointer
    def testFailCreateBridge(self):
        ip = ip_interface(u"192.168.33.10/24")
        self.__interface.sudo("brctl addbr br_" + str(ip.network).split("/")[0])
        with self.assertRaises(RuntimeError):
            b = self.__manager.createBridge(ip.network)

if __name__ == "__main__":
    unittest.main()
