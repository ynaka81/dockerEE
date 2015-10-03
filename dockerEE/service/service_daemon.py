import os
import select
import re
import logging
import Pyro4.core
import Pyro4.naming
from Pyro4.errors import NamingError
from  Pyro4 import socketutil

## ServiceDaemon
#
# The service daemon that provide service interface
class ServiceDaemon(object):
    ## max name server retry
    __retry = 10
    ## constructor
    # @param pidfile The PID filename
    def __init__(self, pidfile):
        # init service parameter
        self.stdin_path = self.stdout_path = self.stderr_path = "/dev/null"
        self.pidfile_timeout = 10
        pidfile = os.path.expanduser(pidfile)
        directory = os.path.dirname(pidfile)
        if not os.path.isdir(directory):
            os.mkdir(directory)
        self.pidfile_path = pidfile
        self.files_preserve = []
        # expose service name
        self.__service_name = str(self.__class__.__name__)
        # prepare exception logger
        self.__exception = logging.getLogger(__name__)
        handler = logging.FileHandler(os.path.join(directory, "exception.log"))
        formatter = logging.Formatter("%(asctime)s; %(name)s; %(message)s")
        handler.setFormatter(formatter)
        self.__exception.addHandler(handler)
        self.files_preserve.append(handler.stream)
    ## the virtual method of application specific initialization before service loop
    # @param self The object pointer
    def _initApp(self):
        pass
    ## the implementation of running application
    # @param self The object pointer
    def run(self):
        try:
            # application specific initialization
            self._initApp()
            # prepare service connection
            uri, name_server, broadcast_server = Pyro4.naming.startNS(host=socketutil.getIpAddress(None, workaround127=True))
            daemon = Pyro4.core.Daemon()
            service_uri = daemon.register(self)
            name_server.nameserver.register(self.__service_name, service_uri)
            # service connection waiting loop
            while True:
                try:
                    # create waiting sockets
                    name_server_sockets = set(name_server.sockets)
                    daemon_sockets = set(daemon.sockets)
                    rs = [broadcast_server]
                    rs.extend(name_server_sockets)
                    rs.extend(daemon_sockets)
                    rs, _, _ = select.select(rs, [], [], 3)
                    # socket processes
                    name_server_events = []
                    daemon_events = []
                    for s in rs:
                        if s is broadcast_server:
                            broadcast_server.processRequest()
                        elif s in name_server_sockets:
                            name_server_events.append(s)
                        elif s in daemon_sockets:
                            daemon_events.append(s)
                    if name_server_events:
                        name_server.events(name_server_events)
                    if daemon_events:
                        daemon.events(daemon_events)
                # unregister myself when service daemon exit
                except SystemExit:
                    daemon.unregister(self)
                    raise
        except Exception, e:
            self.__exception.exception(e)
    ## check if myself is running
    # @param self The object pointer
    def ping(self):
        pass
    ## get myself
    # @param self The object pointer
    # @return my object pointer
    def _getInstance(self):
        instance = Pyro4.core.Proxy("PYRONAME:" + self.__service_name)
        # check if myself is running
        for i in range(self.__retry):
            try:
                instance.ping()
                return instance
            except NamingError as e:
                continue
        raise e
