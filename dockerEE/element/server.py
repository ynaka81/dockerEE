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
    ## execute command on server
    # @param self The object pointer
    # @param command The command to execute on server
    # @return CommandResult
    def command(self, command):
        return self.__container.command(command)
    ## reload myself
    # @param self The object pointer
    def reload(self):
        self.__container.reload()
