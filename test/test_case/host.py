import unittest
from ipaddress import ip_interface
import sys
sys.path.append("/vagrant/dockerEE/host")
from host_manager import HostManager
sys.path.append("../../")
from dockerEE.remote import RemoteInterfaceImpl

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

if __name__ == "__main__":
    unittest.main()
