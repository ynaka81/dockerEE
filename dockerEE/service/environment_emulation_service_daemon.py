import sys
sys.path.append("../../")
from service_daemon import ServiceDaemon
from dockerEE.core import ContainerManagerImpl
from dockerEE.host import HostManagerImpl
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
        ## manager connection info
        self.__conn_info = {"host": host, "user": user, "password": password}
        ## container manager
        self.__container_manager = None
        ## host OS manager
        self.__host_manager = None
        ## environment emulation items
        self.__items = {}
    ## the implementation of application specific initialization before service loop
    # @param self The object pointer
    def _initApp(self):
        # create emulation environment
        self.__container_manager = ContainerManagerImpl(**self.__conn_info)
        self.__host_manager = HostManagerImpl(**self.__conn_info)
        # load environment
        parameter = YamlParser()(sys.argv[2])
        self.__items["servers"] = ServerLoader()(self.__container_manager, self.__host_manager, parameter["servers"])
    ## the implementation of application specific detruction before service stop
    # @param self The object pointer
    def _delApp(self):
        # destroy environment
        for s in self.__items["servers"].values():
            s.destroy()
    ## exposed method of getting item status
    # @param self The object pointer
    # @return item status list
    def getItemStatus(self):
        items = {}
        # server status
        items["servers"] = {}
        for k, v in self.__items["servers"].items():
            items["servers"][k] = {}
            for n in v.getNetworkInfo():
                items["servers"][k][n["dev"]] = str(n["IP"])
                if n["gw"] is not None:
                    items["servers"][k][n["dev"]] += " via " + str(n["gw"])
        return items
    ## exposed method of reloading server
    # @param self The object pointer
    # @param server The reload server name
    def reloadServer(self, server):
        self.__items["servers"][server].reload(self.__container_manager, self.__host_manager)
    ## the implementation of displaying status
    # @param self The object pointer
    # @return The status message
    def getStatus(self):
        try:
            items = self._getInstance().getItemStatus()
            status = "loaded items\n"
            for k1 in sorted(items.keys()):
                v1 = items[k1]
                status += k1 + "\n"
                for k2 in sorted(v1.keys()):
                    v2 = v1[k2]
                    status += "\t" + k2 + "\n"
                    for k3 in sorted(v2.keys()):
                        v3 = v2[k3]
                        status += "\t\t" + k3 + " : " + v3 + "\n"
            return status
        except Exception:
            return "inactive"
    ## the implementation of reloading
    # @param self The object pointer
    def reload(self):
        for server in sys.argv[2:]:
            self._getInstance().reloadServer(server)
