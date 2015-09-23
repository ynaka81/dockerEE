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
    ## inner function of checking whether the container exists
    # @param self The object pointer
    # @param containers The name of containers
    # @param all_exist True:all containers exist, False:all containers not exist
    def __checkContainerExist(self, containers, all_exist):
        if not isinstance(containers, list):
            containers = [containers]
        ret = self.__interface.sudo("docker ps -a")
        lines = ret.stdout.splitlines()[1:]
        for c in containers:
            try:
                (l for l in lines if c in l).next()
                if not all_exist:
                    return False
            except StopIteration:
                if all_exist:
                    return False
        return len(lines) == len(containers) if all_exist else len(lines) == 0
    ## check whether the all containers exist
    # @param self The object pointer
    # @param containers The name of containers
    def checkContainerExist(self, containers):
        return self.__checkContainerExist(containers, True)
    ## check whether the all containers not exist
    # @param self The object pointer
    # @param containers The name of containers
    def checkContainerNotExist(self, containers):
        return self.__checkContainerExist(containers, False)
