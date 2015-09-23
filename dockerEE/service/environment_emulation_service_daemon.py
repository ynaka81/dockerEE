import sys
sys.path.append("../../")
from service_daemon import ServiceDaemon
from dockerEE.core import ContainerManagerImpl
from dockerEE.loader import ServerLoader
from dockerEE.parser import YamlParser

## EnvironmentEmulationServiceDaemon
#
# The service daemon implementation of environment emulation
class EnvironmentEmulationServiceDaemon(ServiceDaemon):
    ## constructor
    # @param host The host to connect
    # @param user The login user
    # @param password The login password
    def __init__(self, host=None, user=None, password=None):
        ServiceDaemon.__init__(self, "~/.dockerEE/environment_emulation_service.pid")
        ## container manager connection info
        self.__conn_info = {"host": host, "user": user, "password": password}
        ## environment emulation items
        self.__items = {}
    ## the implementation of application specific initialization before service loop
    # @param self The object pointer
    def _initApp(self):
        # create emulation environment
        manager = ContainerManagerImpl(**self.__conn_info)
        # load environment
        parameter = YamlParser()(sys.argv[2])
        self.__items["servers"] = ServerLoader()(manager, parameter["servers"])
    ## exposed method of getting item status
    # @param self The object pointer
    # @return item status list
    def getItemStatus(self):
        items = {}
        # server status
        items["servers"] = {}
        for k, v in self.__items["servers"].items():
            items["servers"][k] = {}
        return items
    ## exposed method of reloading server
    # @param self The object pointer
    # @param server The reload server name
    def reloadServer(self, server):
        self.__items["servers"][server].reload()
    ## the implementation of displaying status
    # @param self The object pointer
    # @return The status message
    def getStatus(self):
        items = self._getInstance().getItemStatus()
        status = "loaded items\n"
        for k1, v1 in items.items():
            status += k1 + "\n"
            for k2, v2 in v1.items():
                status += "\t" + k2 + "\n"
                for k3, v3 in v2.items():
                    status += "\t\t" + k3 + ":" + v3 + "\n"
        return status
    ## the implementation of reloading
    # @param self The object pointer
    def reload(self):
        self._getInstance().reloadServer(sys.argv[2])
