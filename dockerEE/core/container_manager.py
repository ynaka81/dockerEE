from abc import ABCMeta, abstractmethod
from weakref import WeakSet

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
        self.__manager.createContainerImpl(self, **options)
    ## destructor
    def __del__(self):
        if self.__manager is not None:
            self.destroy()
    ## check if the container is destroy
    # @param self The object pointer
    def __checkDestroyed(self):
        if self.__manager is None:
            raise RuntimeError("The conainer(" + self.__name + ") is already destroyed.")
    ## destroy container
    # @param self The object pointer
    def destroy(self):
        if self.__manager is not None:
            # destroy myself
            self.__manager.destroyContainerImpl(self)
            # initialize variables
            self.__manager = None
    ## get container name
    # @param self The object pointer
    def getName(self):
        self.__checkDestroyed()
        return self.__name
    ## get container options
    # @param self The object pointer
    # @return container options
    def getOptions(self):
        self.__checkDestroyed()
        return self.__options
    ## execute command on container
    # @param self The object pointer
    # @param command The command to execute on container
    # @return CommandResult
    def command(self, command):
        self.__checkDestroyed()
        return self.__manager.command(self, command)
    ## attach IP to container
    # @param self The object pointer
    # @param segment The name of the segment which the IP is attached on
    # @param dev The device name of container
    # @param IP The IP attached to the container
    # @param gw The gateway address if the device is default gateway
    def attachIP(self, segment, dev, IP, gw=None):
        self.__checkDestroyed()
        self.__manager.attachIP(self, segment, dev, IP, gw)

## ContainerManager
#
# The interface class to control container
class ContainerManager(object):
    __metaclass__ = ABCMeta
    ## weak reference of container
    __container = WeakSet()
    ## abstract method of creating container
    # @param self The object pointer
    # @param container The container that will be created
    # @param options The options to create container
    @abstractmethod
    def createContainerImpl(self, container, **options):
        pass
    ## abstract method of destroying container
    # @param self The object pointer
    # @param container The container that will be created
    @abstractmethod
    def destroyContainerImpl(self, container):
        pass
    ## abstract method of executing command on container
    # @param self The object pointer
    # @param container The container that will be created
    # @param command The command to execute on container
    # @return CommandResult
    @abstractmethod
    def command(self, container, command):
        pass
    ## abstract method of attaching IP to container
    # @param self The object pointer
    # @param container The container that will be created
    # @param segment The name of the segment which the IP is attached on
    # @param dev The device name of container
    # @param IP The IP attached to the container
    # @param gw The gateway address if the device is default gateway
    @abstractmethod
    def attachIP(self, container, segment, dev, IP, gw):
        pass
    ## create container
    # @param self The object pointer
    # @param name The name of container
    # @param options The options to create container
    # @return container
    def create(self, name, **options):
        # raise exception if the container already exists
        try:
            (c for c in self.__container if c.getName() == name).next()
            raise ValueError("The container (" + name + ") is already running.")
        except StopIteration:
            c = Container(self, name, **options)
            self.__container.add(c)
            return c
