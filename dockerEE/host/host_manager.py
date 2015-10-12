from abc import ABCMeta, abstractmethod
from weakref import WeakSet

## Bridge
#
# The host OS bridge class
class Bridge(object):
    ## constructor
    # @param manager The manager implement class to control host OS
    # @param network_address The network address of the bridge
    def __init__(self, manager, network_address):
        ## host OS manager
        self.__manager = manager
        ## network address
        self.__network_address = network_address
        # create myself
        self.__manager.createBridgeImpl(self)
    ## destructor
    def __del__(self):
        # destroy myself
        self.__manager.destroyBridgeImpl(self)
    ## get bridge network address
    # @param self The object pointer
    def getNetworkAddress(self):
        return self.__network_address
    ## get name
    def getName(self):
        return "br_" + str(self.__network_address).split("/")[0]

## HostManager
#
# The interface class to control host OS
class HostManager(object):
    __metaclass__ = ABCMeta
    ## weak reference of host OS bridge
    __bridge = WeakSet()
    ## abstract method of creating bridge
    # @param self The object pointer
    # @param bridge The bridge that will be created
    @abstractmethod
    def createBridgeImpl(self, bridge):
        pass
    ## abstract method of destroying container
    # @param self The object pointer
    # @param bridge The bridge that will be deleted
    @abstractmethod
    def destroyBridgeImpl(self, bridge):
        pass
    ## create bridge
    # @param self The object pointer
    # @param network_address The network address of the bridge
    # @return bridge
    def createBridge(self, network_address):
        # only when the network address does not exist in created container, new one is created
        try:
            return (b for b in self.__bridge if b.getNetworkAddress() == network_address).next()
        except StopIteration:
            b = Bridge(self, network_address)
            self.__bridge.add(b)
            return b
