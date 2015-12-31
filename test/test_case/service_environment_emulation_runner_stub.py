import sys
sys.path.append("/vagrant/dockerEE/service")

import os
import time

from environment_emulation_runner import EnvironmentEmulationRunner

## TestDaemon
#
# The test daemon class
class TestDaemon(object):
    ## constructor
    def __init__(self):
        self.stdin_path = self.stdout_path = self.stderr_path = "/dev/null"
        self.pidfile_timeout = 3
        self.directory = os.path.expanduser("~/.dockerEE/")
        if not os.path.isdir(self.directory):
            os.mkdir(self.directory)
        self.pidfile_path = os.path.join(self.directory, "test_service_environment_emulation_runner.pid")
    ## the implementation of running application
    # @param self The object pointer
    def run(self):
        while True:
            time.sleep(1)
    ## the implementation of displaying status
    # @param self The object pointer
    # @return The status message
    def getStatus(self):
        return "OK"
    ## the implementation of reloading
    # @param self The object pointer
    def reload(self):
        print "reloaded"

if __name__ == "__main__":
    daemon_runner = EnvironmentEmulationRunner(TestDaemon())
    daemon_runner.do_action()
