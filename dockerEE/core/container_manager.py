from abc import ABCMeta, abstractmethod

## Container
#
# The container class
class Container(object):
    ## constructor
    # @param manager The manager implement class to control container
    # @param name The name of container
    # @param options The options to create container
    def __init__(self, manager, name, **options):
        ## container name
        self.__name = name
        ## container manager
        self.__manager = manager
        ## container create options
        self.__options = options
        # create myself
        self.__manager.createContainer(self.__name, **options)
    ## destructor
    def __del__(self):
        # destroy myself
        self.__manager.destroyContainer(self.__name)
    ## get container name
    # @param self The object pointer
    def getName(self):
        return self.__name
    ## get container options
    # @param self The object pointer
    # @return container options
    def getOptions(self):
        return self.__options
    ## execute command on container
    # @param self The object pointer
    # @param command The command to execute on container
    # @return CommandResult
    def command(self, command):
        return self.__manager.command(self.__name, command)

## ContainerManager
#
# The interface class to control container
class ContainerManager(object):
    __metaclass__ = ABCMeta
    ## abstract method of creating container
    # @param self The object pointer
    # @param name The name of container
    # @param options The options to create container
    @abstractmethod
    def createContainer(self, name, **options):
        pass
    ## abstract method of destroying container
    # @param self The object pointer
    # @param name The name of container
    @abstractmethod
    def destroyContainer(self, name):
        pass
    ## abstractmethod of executing command on container
    # @param self The object pointer
    # @param name The name of container
    # @param command The command to execute on container
    # @return CommandResult
    @abstractmethod
    def command(self, name, command):
        pass
    ## create container
    # @param self The object pointer
    # @param name The name of container
    # @param options The options to create container
    # @return container
    def create(self, name, **options):
        return Container(self, name, **options)
