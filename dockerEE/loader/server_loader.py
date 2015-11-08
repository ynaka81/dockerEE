from ipaddress import ip_interface
from dockerEE.element import Server

## ServerLoader
#
# The loader of server elements
class ServerLoader(object):
    ## load the server definition
    # @param self The object pointer
    # @param container_manager The container manager
    # @param host_manager The host OS manager
    # @param parameter The denifition of server
    def __call__(self, container_manager, host_manager, parameter):
        servers = {}
        for p in parameter:
            server = Server(container_manager, p["name"], source=p["image"])
            for n in p.get("IPs", []):
                if "gw" in n:
                    server.attachIP(host_manager, n["dev"], ip_interface(unicode(n["IP"])), ip_interface(unicode(n["gw"])))
                else:
                    server.attachIP(host_manager, n["dev"], ip_interface(unicode(n["IP"])))
            servers[server.getName()] = server
        return servers
