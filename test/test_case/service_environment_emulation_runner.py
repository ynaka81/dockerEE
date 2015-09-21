import unittest
import sys
sys.path.append("../../")
import time
from dockerEE.remote import RemoteInterfaceImpl

## TestEnvironmentEmulationRunner
#
# The test case for EnvironmentEmulationRunner
class TestEnvironmentEmulationRunner(unittest.TestCase):
    ## execute stub
    # @param self The object pointer
    # @param action The action
    # @return CommandResult
    def __execStub(self, action):
        return self.__interface.sudo("cd /vagrant/test/test_case/; python " + self.__stub + " " + action, True)
    ## init test case
    # @param self The object pointer
    def setUp(self):
        ## remote interface
        self.__interface = RemoteInterfaceImpl("localhost", "vagrant", "vagrant", pty=False)
        ## stub file
        self.__stub = "service_environment_emulation_runner_stub.py"
    ## test "python service.py"
    # @param self The object pointer
    def testUsage(self):
        ret = self.__execStub("")
        self.assertEqual(ret.stdout, "usage: " + self.__stub + " " + "|".join({"start":None, "stop":None, "restart":None, "status":None, "reload":None}.keys()))
    ## test "python service.py status"
    # @param self The object pointer
    def testStatus(self):
        ret = self.__execStub("status")
        self.assertIn("Active: inactive (dead)", ret.stdout)
        ret = self.__execStub("start")
        ret = self.__execStub("status")
        self.assertIn("Active: active (running)", ret.stdout)
        self.assertIn("App Specific: OK", ret.stdout)
        ret = self.__execStub("stop")
        ret = self.__execStub("status")
        self.assertIn("Active: inactive (dead)", ret.stdout)
    ## test "python service.py reload"
    # @param self The object pointer
    def testReload(self):
        ret = self.__execStub("start")
        ret = self.__execStub("reload")
        self.assertEqual(ret.stdout, "reloaded")
        ret = self.__execStub("stop")

    ## test "python service.py reload" fail bacause the service is not normally running
    # @param self The object pointer
    def testFailReload(self):
        ret = self.__execStub("reload")
        self.assertEqual(ret.rc, 1)

if __name__ == "__main__":
    unittest.main()
