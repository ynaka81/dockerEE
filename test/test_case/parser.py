import unittest
import sys
sys.path.append("../../")
from dockerEE.parser import YamlParser

## TestYamlParser
#
# The test case for YamlParser
class TestYamlParser(unittest.TestCase):
    ## test YamlParser.__call__(env_file)
    # @param self The object pointer
    def testCall(self):
        parameter = [{"name": "c1", "image": "centos"}, {"name": "c2", "image": "centos"}]
        yaml_file = "/tmp/test.yml"
        f = open(yaml_file, "w")
        f.write("---\n")
        f.write("servers:\n")
        for p in parameter:
            f.write("- name: " + p["name"] + "\n")
            f.write("  image: " + p["image"] + "\n")
        f.close()
        parser = YamlParser()
        parsed_parameter = parser(yaml_file)
        self.assertEqual(parameter, parsed_parameter["servers"])

if __name__ == "__main__":
    unittest.main()
