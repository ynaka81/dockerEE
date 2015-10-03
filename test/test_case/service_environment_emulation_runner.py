import unittest
import sys
sys.path.append("../../")
import time
from service_test_utils import ServiceTestUtils
from dockerEE.remote import RemoteInterfaceImpl

## TestEnvironmentEmulationRunner
#
# The test case for EnvironmentEmulationRunner
class TestEnvironmentEmulationRunner(unittest.TestCase):
    ## init test case
    # @param self The object pointer
    def setUp(self):
        ## stub file
        self.__stub = "service_environment_emulation_runner_stub.py"
        ## service test utils
        self.__service = ServiceTestUtils("python /vagrant/test/test_case/" + self.__stub, "localhost", "vagrant", "vagrant")
        ## starting file name
        self.__filename = "/tmp/service_environment_emulation_runner"
        open(self.__filename, "w")
    ## test "python service.py"
    # @param self The object pointer
    def testUsage(self):
        ret = self.__service.usage()
        self.assertIn("usage: " + self.__stub + " " + "|".join({"start":None, "stop":None, "restart":None, "status":None, "reload":None}.keys()), ret.stdout)
        self.assertIn("options:", ret.stdout)
    ## test "python service.py start"
    def testStart(self):
        ret = self.__service.start(self.__filename)
        self.assertEqual(ret.rc, 0)
        ret = self.__service.stop()
        self.assertEqual(ret.rc, 0)
    ## test "python service.py status"
    # @param self The object pointer
    def testStatus(self):
        ret = self.__service.status()
        self.assertIn("Active: inactive (dead)", ret.stdout)
        self.assertNotIn("App Specific:", ret.stdout)
        self.__service.start(self.__filename)
        ret = self.__service.status()
        self.assertIn("Active: active (running)", ret.stdout)
        self.assertIn("App Specific: OK", ret.stdout)
        self.__service.stop()
        ret = self.__service.status()
        self.assertIn("Active: inactive (dead)", ret.stdout)
        self.assertNotIn("App Specific:", ret.stdout)
    ## test "python service.py reload"
    # @param self The object pointer
    def testReload(self):
        self.__service.start(self.__filename, 10)
        ret = self.__service.reload()
        self.assertEqual(ret.stdout, "reloaded")
        self.__service.stop()

    ## test "python service.py start" fail because 3rd argument is none
    # @param self The object pointer
    def testFailStart3rdNone(self):
        ret = self.__service.start("")
        self.assertNotEqual(ret.rc, 0)
    ## test "python service.py start" fail because invalid file name
    # @param self The object pointer
    def testFailStartInvalidFileName(self):
        ret = self.__service.start("/tmp/not_exist_file")
        self.assertNotEqual(ret.rc, 0)
    ## test "python service.py reload" fail bacause the service is not normally running
    # @param self The object pointer
    def testFailReload(self):
        ret = self.__service.reload()
        self.assertEqual(ret.rc, 1)

if __name__ == "__main__":
    unittest.main()
