from dockerEE.element import Server

## ServerLoader
#
# The loader of server elements
class ServerLoader(object):
    ## load the server definition
    # @param self The object pointer
    # @param manager The container manager
    # @param parameter The denifition of server
    def __call__(self, manager, parameter):
        servers = {}
        for p in parameter:
            server = Server(manager, p["name"], source=p["image"])
            servers[server.getName()] = server
        return servers
