from environment_emulation_runner import EnvironmentEmulationRunner
from environment_emulation_service_daemon import EnvironmentEmulationServiceDaemon

## EnvironmentEmulationService
#
# The service interface of environment emulation
class EnvironmentEmulationService(object):
    ## constructor
    # @param host The host to connect
    # @param user The login user
    # @param password The login password
    def __init__(self, host=None, user=None, password=None):
        ## environment emulation runner
        self.__runner = EnvironmentEmulationRunner(EnvironmentEmulationServiceDaemon(host, user, password))
    ## execute action
    # @param self The object pointer
    def action(self):
        self.__runner.do_action()
