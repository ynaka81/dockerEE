import sys
sys.path.append("../../")
import os
import time
from dockerEE.core import ContainerManagerImpl
from dockerEE.loader import ServerLoader
from dockerEE.parser import YamlParser

## EnvironmentEmulationServiceDaemon
#
# The service daemon implementation of environment emulation
class EnvironmentEmulationServiceDaemon(object):
    ## constructor
    # @param host The host to connect
    # @param user The login user
    # @param password The login password
    def __init__(self, host=None, user=None, password=None):
        # init service parameter
        self.stdin_path = self.stdout_path = self.stderr_path = "/dev/null"
        self.pidfile_timeout = 10
        self.directory = os.path.expanduser("~/.dockerEE/")
        if not os.path.isdir(self.directory):
            os.mkdir(self.directory)
        self.pidfile_path = os.path.join(self.directory, "environment_emulation_service.pid")
        ## container manager connection info
        self.__conn_info = {"host": host, "user": user, "password": password}
        ## environment emulation items
        self.__items = {}
    ## the implementation of running application
    # @param self The object pointer
    def run(self):
        # create emulation environment
        manager = ContainerManagerImpl(**self.__conn_info)
        # load environment
        parameter = YamlParser()(sys.argv[2])
        self.__items["servers"] = ServerLoader()(manager, parameter["servers"])
        # neet loop
        while True:
            time.sleep(1)
    ## the implementation of displaying status
    # @param self The object pointer
    # @return The status message
    def getStatus(self):
        return None
    ## the implementation of reloading
    # @param self The object pointer
    def reload(self):
        pass
