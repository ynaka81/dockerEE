import sys
sys.path.append("../../")
from dockerEE.remote import RemoteInterfaceImpl

## DockerContainerTestUtils
#
# The test utils of docker container
class DockerContainerTestUtils(object):
    ## constructor
    # @param host The host to connect
    # @param user The login user
    # @param password The login password
    def __init__(self, host=None, user=None, password=None): 
        ## remote interface
        self.__interface = RemoteInterfaceImpl(host, user, password)
    ## check whether the container exists
    # @param self The object pointer
    # @param containers The name of containers
    def checkContainerExist(self, containers):
        if not isinstance(containers, list):
            containers = [containers]
        ret = self.__interface.sudo("docker ps -a")
        lines = ret.stdout.splitlines()[1:]
        for c in containers:
            try:
                (l for l in lines if c in l).next()
            except StopIteration:
                return False
        return len(lines) == len(containers)
