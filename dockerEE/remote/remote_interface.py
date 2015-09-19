from abc import ABCMeta, abstractmethod

## CommandResult
#
# The command return structure
class CommandResult(object):
    ## constructor
    # @param command The command to execute
    # @param rc The return code of command
    # @param stdout The standard output
    # @param stderr The standard error
    def __init__(self, command, rc, stdout, stderr):
        ## command
        self.command = command
        ## return code
        self.rc = rc
        ## stdout
        self.stdout = stdout
        ## stderr
        self.stderr = stderr

## RemoteInterface
#
# The interface class to execute commands on remote hosts
class RemoteInterface(object):
    __metaclass__ = ABCMeta
    ## run command with sudo
    # @param self The object pointer
    # @param command The command to execute
    # @param ignore_error Whether the error is ignored or not
    # @return CommandResult
    @abstractmethod
    def sudo(self, command, ignore_error=False):
        pass
