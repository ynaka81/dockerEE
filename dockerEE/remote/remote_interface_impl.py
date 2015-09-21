import fabric.api
from fabric.context_managers import hide, warn_only, settings
from fabric.network import disconnect_all
from remote_interface import RemoteInterface, CommandResult

## RemoteInterfaceImpl
#
# The fabric implementaion of RemoteInterface
class RemoteInterfaceImpl(RemoteInterface):
    ## constructor
    # @param host The host to connect
    # @param user The login user
    # @param password The login password
    # @param pty Whether pty is used or not
    def __init__(self, host=None, user=None, password=None, pty=True):
        ## pty option
        self.__pty = pty
        # set target info to fabric
        fabric.api.env.host_string = host
        fabric.api.env.user = user
        fabric.api.env.password = password
    ## destructor
    def __del__(self):
        # close fabric connetction
        disconnect_all()
    ## run command with sudo
    # @param self The object pointer
    # @param command The command to execute
    # @param ignore_error Whether the error is ignored or not
    # @return CommandResult
    def sudo(self, command, ignore_error=False):
        hide_parameter = ["running", "stdout"]
        if ignore_error:
            hide_parameter += ["stderr", "warnings"]
            settings_parameter = {"warn_only":True}
        else:
            settings_parameter = {}
        with settings(hide(*hide_parameter), **settings_parameter):
            ret = fabric.api.sudo(command, pty=self.__pty)
        return CommandResult(ret.command, ret.return_code, ret.stdout, ret.stderr)
