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
    # @param network_address The network address of the bridge
    def createBridgeImpl(self, network_address):
        name = "br_" + str(network_address).split("/")[0]
        # create a new bridge
        for cmd in ("brctl addbr " + name, "ip link set " + name + " up"):
            ret = self.__interface.sudo(cmd, True)
            if ret.rc != 0:
                raise RuntimeError("Cannot create bridge(" + str(network_address) + "): " + ret.stdout + ret.stderr)
    ## the implementation of deleting bridge
    # @param self The object pointer
    # @param network_address The network address of the bridge
    def destroyBridgeImpl(self, network_address):
        name = "br_" + str(network_address).split("/")[0]
        # destroy the bridge
        for cmd in ("ip link set " + name + " down", "brctl delbr " + name):
            ret = self.__interface.sudo(cmd, True)
            if ret.rc != 0:
                raise RuntimeError("Cannot destroy bridge(" + str(network_address) + "): " + ret.stdout + ret.stderr)
