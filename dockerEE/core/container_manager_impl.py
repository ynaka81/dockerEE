from container_manager import ContainerManager
from dockerEE.remote import RemoteInterfaceImpl

## ContainerManagerImpl
#
# The docker implementaion of ContainerManager
class ContainerManagerImpl(ContainerManager):
    ## constructor
    # @param host The host to connect
    # @param user The login user
    # @param password The login password
    def __init__(self, host=None, user=None, password=None):
        ## remote interface
        self.__interface = RemoteInterfaceImpl(host, user, password)
        ## host name list
        self.__host_name = []
        # check if docker service is running
        if self.__interface.sudo("docker info", True).rc != 0:
            raise RuntimeError("The docker service is not running at " + host)
    ## destructor
    def __del__(self):
        # destroy the containers still running
        for h in self.__host_name:
            self.destroyContainer(h)
    ## create container
    # @param self The object pointer
    # @param name The name of container
    # @param privilege The privilege attached to docker container
    # @param image The image of container
    def createContainer(self, name, privilege=["NET_ADMIN"], hosts=[], image="centos"):
        if name in self.__host_name:
            raise ValueError("The host name(" + name + ") is already running.")
        cmd = "docker run --name=" + name + " --hostname=" + name + " --net=none"
        # add privilege
        for p in privilege:
            cmd += " --cap-add " + p
        # add hosts
        for h in hosts:
            cmd += " --add-host " + h["name"] + ":" + h["IP"]
        # create a new containter
        cmd += " -itd " + image + " /bin/bash"
        ret = self.__interface.sudo(cmd, True)
        if ret.rc != 0:
            raise RuntimeError("Cannot create container(" + name + "): " + ret.stderr)
        # add to the host name list
        self.__host_name.append(name)
    ## delete container
    # @param self The object pointer
    # @param name The name of container
    def destroyContainer(self, name):
        if name not in self.__host_name:
            raise ValueError("The host name(" + name + ") is not running yet.")
        # destroy the container
        ret = self.__interface.sudo("docker rm -f " + name, True)
        if ret.rc != 0:
            raise RuntimeError("Cannot destroy container(" + name + "): " + ret.stderr)
        # delete from host name list
        self.__host_name.remove(name)
