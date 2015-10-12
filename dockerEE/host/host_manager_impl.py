from host_manager import HostManager
from dockerEE.remote import RemoteInterfaceImpl

## HostManagerImpl
#
# The command line implementation of HostManager
class HostManagerImpl(HostManager):
    ## constructor
    # @param host The host to connect
    # @param user The login user
    # @param password The login password
    def __init__(self, host=None, user=None, password=None):
        ## remote interface
        self.__interface = RemoteInterfaceImpl(host, user, password)
    ## the implementation of creating bridge
    # @param self The object pointer
    # @param bridge The bridge that will be created
    def createBridgeImpl(self, bridge):
        # create a new bridge
        for cmd in ("brctl addbr " + bridge.getName(), "ip link set " + bridge.getName() + " up"):
            ret = self.__interface.sudo(cmd, True)
            if ret.rc != 0:
                raise RuntimeError("Cannot create bridge(" + str(bridge.getNetworkAddress()) + "): " + ret.stdout + ret.stderr)
    ## the implementation of deleting bridge
    # @param self The object pointer
    # @param bridge The bridge that will be deleted
    def destroyBridgeImpl(self, bridge):
        # destroy the bridge
        for cmd in ("ip link set " + bridge.getName() + " down", "brctl delbr " + bridge.getName()):
            ret = self.__interface.sudo(cmd, True)
            if ret.rc != 0:
                raise RuntimeError("Cannot destroy bridge(" + str(bridge.getNetworkAddress()) + "): " + ret.stdout + ret.stderr)
