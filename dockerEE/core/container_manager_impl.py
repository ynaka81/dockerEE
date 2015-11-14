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
        # check if docker service is running
        if self.__interface.sudo("docker info", True).rc != 0:
            raise RuntimeError("The docker service is not running at " + host)
    ## create container
    # @param self The object pointer
    # @param container The container that will be created
    # @param privilege The privilege attached to docker container
    # @param image The image of container
    def createContainerImpl(self, container, privilege=["NET_ADMIN"], hosts=[], image="centos"):
        cmd = "docker run --name=" + container.getName() + " --hostname=" + container.getName() + " --net=none"
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
            raise RuntimeError("Cannot create container(" + container.getName() + "): " + ret.stderr)
    ## delete container
    # @param self The object pointer
    # @param container The container that will be created
    def destroyContainerImpl(self, container):
        # destroy the container
        ret = self.__interface.sudo("docker rm -f " + container.getName(), True)
        if ret.rc != 0:
            raise RuntimeError("Cannot destroy container(" + container.getName() + "): " + ret.stderr)
    ## execute command on container
    # @param self The object pointer
    # @param container The container that will be created
    # @param command The command to execute on container
    # @return CommandResult
    def command(self, container, command):
        # execute command on container
        ret = self.__interface.sudo("docker exec -it " + container.getName() + " " + command, True)
        if ret.rc != 0:
            raise RuntimeError("Failed to execute command(\"" + command + "\") on container(" + container.getName() + "): " + ret.stderr)
        return ret
    ## attach IP to container
    # @param self The object pointer
    # @param container The container that will be created
    # @param segment The name of the segment which the IP is attached on
    # @param dev The device name of container
    # @param IP The IP attached to the container
    # @param gw The gateway address if the device is default gateway
    def attachIP(self, container, segment, dev, IP, gw):
        # execute pipework to attach IP to container
        cmd = "/usr/local/bin/pipework " + segment + " -i " + dev + " " + container.getName() + " " + str(IP)
        if gw:
            cmd += "@" + str(gw.ip)
        ret = self.__interface.sudo(cmd, True)
        if ret.rc != 0:
            raise RuntimeError("Failed to attach IP(" + str(IP) + ") to the container(" + container.getName() + "): " + ret.stdout + ret.stderr)
