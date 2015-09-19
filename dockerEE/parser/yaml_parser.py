import yaml

## YamlParser
#
# The yaml parser of the environment emulation definitions
class YamlParser(object):
    ## parse environment form yaml file
    # @param self The object pointer
    # @param env_file The environment definition yaml file
    # @return The parsed parameter
    def __call__(self, env_file):
        parameter = yaml.load(file(env_file))
        return parameter
