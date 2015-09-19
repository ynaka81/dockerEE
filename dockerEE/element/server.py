## Server
#
# The server emulation
class Server(object):
    ## constructor
    # @param manager The container manager
    # @param name The name of container
    # @param source The source image of the server
    def __init__(self, manager, name, source="centos"):
        ## server container
        self.__container = manager.create(name, image=source)
    ## get server name
    # @param self The object pointer
    def getName(self):
        return self.__container.getName()
