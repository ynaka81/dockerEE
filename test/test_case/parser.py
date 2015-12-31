import sys
sys.path.append("../../")

import unittest

from dockerEE.parser import YamlParser

## TestYamlParser
#
# The test case for YamlParser
class TestYamlParser(unittest.TestCase):
    ## test YamlParser.__call__(env_file)
    # @param self The object pointer
    def testCall(self):
        parameter = [{"name": "s1", "image": "local/centos"}, {"name": "s2", "image": "local/centos"}]
        yaml_file = "/tmp/test.yml"
        f = open(yaml_file, "w")
        f.write("---\n")
        f.write("servers:\n")
        for p in parameter:
            f.write("        - name: " + p["name"] + "\n")
            f.write("          image: " + p["image"] + "\n")
        f.close()
        parser = YamlParser()
        parsed_parameter = parser(yaml_file)
        self.assertEqual(parsed_parameter["servers"], parameter)

if __name__ == "__main__":
    unittest.main()
