import sys

## Server
#
# The server emulation
class Server(object):
    ## constructor
    # @param container_manager The container manager
    # @param name The name of container
    # @param source The source image of the server
    def __init__(self, container_manager, name, source="centos"):
        ## server container
        self.__container = container_manager.create(name, image=source)
        ## network info
        self.__network = []
    ## check if the server is destroy
    # @param self The object pointer
    def __checkDestroyed(self):
        if self.__container is None and self.__network is None:
            raise RuntimeError("The server is already destroyed.")
    ## destroy server
    # @param self The object pointer
    def destroy(self):
        if self.__container is not None:
            # destroy container
            self.__container.destroy()
            # destroy bridge if refcount is 1
            for n in self.__network:
                if sys.getrefcount(n["segment"]) - 1 == 1:
                    n["segment"].destroy()
            # initialize variables
            self.__container = self.__network = None
    ## get server name
    # @param self The object pointer
    def getName(self):
        self.__checkDestroyed()
        return self.__container.getName()
    ## execute command on server
    # @param self The object pointer
    # @param command The command to execute on server
    # @return CommandResult
    def command(self, command):
        self.__checkDestroyed()
        return self.__container.command(command)
    ## attach IP to server
    # @param self The object pointer
    # @param host_manager The host OS manager
    # @param dev The device name of the server
    # @param IP The IP attached to the server
    # @param gw The gateway address if the device is default gateway
    def attachIP(self, host_manager, dev, IP, gw=None):
        self.__checkDestroyed()
        # create bridge for network segment
        bridge = host_manager.createBridge(IP.network)
        # add to network info
        self.__network.append({"segment": bridge, "dev": dev, "IP": IP, "gw": gw})
        # attach IP to the server container
        self.__container.attachIP(bridge.getName(), dev, IP, gw)
    ## reload myself
    # @param self The object pointer
    # @param container_manager The container manager
    # @param host_manager The host OS manager
    def reload(self, container_manager, host_manager):
        self.__checkDestroyed()
        # delete and create container
        name = self.getName()
        options = self.__container.getOptions()
        self.__container.destroy()
        self.__container = container_manager.create(name, **options)
        # attach IP
        for n in self.__network:
            self.__container.attachIP(n["segment"].getName(), n["dev"], n["IP"], n["gw"])
