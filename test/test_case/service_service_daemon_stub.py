import sys
sys.path.append("../../dockerEE/service")
import os
import time
from environment_emulation_runner import EnvironmentEmulationRunner
from service_daemon import ServiceDaemon

## TestService
#
# The test service daemon class
class TestService(ServiceDaemon):
    ## constructor
    def __init__(self):
        ServiceDaemon.__init__(self, "~/.dockerEE/test_service_service_daemon.pid")
        ## check file whether destrustor is called
        self.__check_file = file(os.path.expanduser("~/.dockerEE/test_service_service_daemon.check"), "w")
    ## destrustor
    def __del__(self):
        os.remove(self.__check_file.name)
    ## the implementation of application specific initialization before service loop
    # @param self The object pointer
    def _initApp(self):
        self.__counter = 0
    ## get counter
    # @param self The object pointer
    # @return counter
    def getCount(self):
        return self.__counter
    ## count up counter
    # @param self The object pointer
    def countUp(self):
        self.__counter += 1
    ## the implementation of displaying status
    # @param self The object pointer
    # @return The status message
    def getStatus(self):
        return "counter = " + str(self._getInstance().getCount())
    ## the implementation of reloading
    # @param self The object pointer
    def reload(self):
        self._getInstance().countUp()

if __name__ == "__main__":
    service = EnvironmentEmulationRunner(TestService())
    service.do_action()
