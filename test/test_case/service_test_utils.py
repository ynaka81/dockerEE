import sys
sys.path.append("../../")

import time

from dockerEE.remote import RemoteInterfaceImpl

## ServiceTestUtils
#
# The test utils of service
class ServiceTestUtils(object):
    ## delta time for waiting
    __dt = 0.1
    ## constructor
    # @param service_name The service name
    # @param host The host to connect
    # @param user The login user
    # @param password The login password
    def __init__(self, service_name, host=None, user=None, password=None): 
        ## service name
        self.__name = service_name
        ## remote interface
        self.__interface = RemoteInterfaceImpl(host, user, password, pty=False)
    ## display service usage
    # @param self The object pointer
    # @return CommandResult
    def usage(self):
        return self.__interface.sudo(self.__name, True)
    ## start service and wait for starting
    # @param self The object pointer
    # @param start_file The service starting file
    # @param timeout The timeout of waiting for service. When timeout is -1, timeout does not work
    # @return CommandResult
    def start(self, start_file, timeout=-1):
        ret = self.__interface.sudo(self.__name + " start " + start_file, True)
        while timeout > 0 and "active (running)" not in self.__interface.sudo(self.__name + " status").stdout:
            time.sleep(self.__dt)
            timeout -= self.__dt
            if timeout < 0:
                raise RuntimeError("The service (" + self.__name + ") can not be started.")
        return ret
    ## stop service and wait for stopping
    # @param self The object pointer
    # @param timeout The timeout of waiting for service. When timeout is -1, timeout does not work
    # @return CommandResult
    def stop(self, timeout=-1):
        ret = self.__interface.sudo(self.__name + " stop", True)
        while timeout > 0 and "inactive (dead)" not in self.__interface.sudo(self.__name + " status").stdout:
            time.sleep(self.__dt)
            timeout -= self.__dt
            if timeout < 0:
                raise RuntimeError("The service (" + self.__name + ") can not be stopped.")
        return ret
    ## get service status
    # @param self The object pointer
    # @return CommandResult
    def status(self):
        return self.__interface.sudo(self.__name + " status", True)
    ## reload service
    # @param self The object pointer
    # @param argv The reload options
    # @return CommandResult
    def reload(self, argv=[]):
        return self.__interface.sudo(self.__name + " reload " + " ".join(argv), True)
