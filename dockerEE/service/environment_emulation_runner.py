from daemon import runner

## EnvironmentEmulationRunner
#
# The extension of python-daemon.runner for additional actions
class EnvironmentEmulationRunner(runner.DaemonRunner):
    ## constructor
    # @param The daemon application
    def __init__(self, app):
        runner.DaemonRunner.__init__(self, app)
        ## status messages
        self.__status = {"active": "active (running)", "fail": "failed", "inactive": "inactive (dead)"}
        # add runner.DaemonRunner.files_preserve if app has files_preserve
        if hasattr(app, "files_preserve"):
            self.daemon_context.files_preserve = app.files_preserve
    ## display status
    # @param self The object pointer
    def _status(self):
        # the service is not running
        if not self.pidfile.is_locked():
            status = "inactive"
        # the service is failed to start
        elif runner.is_pidfile_stale(self.pidfile):
            status = "fail"
        # the service is running
        else:
            status = "active"
        # display the status
        print "       Active:", self.__status[status]
        print "     Main PID:", self.pidfile.read_pid()
        # display the application specific status when service is running
        if status == "active":
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
