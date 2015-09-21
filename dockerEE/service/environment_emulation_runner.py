from daemon import runner

## EnvironmentEmulationRunner
#
# The extension of python-daemon.runner for additional actions
class EnvironmentEmulationRunner(runner.DaemonRunner):
    ## display status
    # @param self The object pointer
    def _status(self):
        # the service is not running
        if not self.pidfile.is_locked():
            status = "inactive (dead)"
        # the service is failed to start
        elif runner.is_pidfile_stale(self.pidfile):
            status = "failed"
        # the service is running
        else:
            status = "active (running)"
        # display the status
        print "       Active:", status
        print "     Main PID:", self.pidfile.read_pid()
        # display the application specific status
        print ""
        print " App Specific:", self.app.getStatus()
    ## reload environment emulation element
    # @param self The object pointer
    def _reload(self):
        # the service is running
        if self.pidfile.is_locked() and not runner.is_pidfile_stale(self.pidfile):
            self.app.reload()
        # the service is not running
        else:
            raise RuntimeError("The service is not normally running.")
    # add enable actions
    runner.DaemonRunner.action_funcs[u"status"] = _status
    runner.DaemonRunner.action_funcs[u"reload"] = _reload