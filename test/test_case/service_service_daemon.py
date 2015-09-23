import unittest
import sys
sys.path.append("../../")
import time
from dockerEE.remote import RemoteInterfaceImpl
from service_service_daemon_stub import TestService

## TestServerDaemon
#
# The test case for ServiceDaemon
class TestServiceDaemon(unittest.TestCase):
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
        self.__stub = "service_service_daemon_stub.py"
    ## test "python service.py start/stop"
    # @param self The object pointer
    def testStartStop(self):
        ret = self.__execStub("start /tmp/env.yml")
        self.assertEqual(ret.rc, 0)
        ret = self.__interface.sudo("test -f ~/.dockerEE/test_service_service_daemon.check", True)
        self.assertEqual(ret.rc, 0)
        time.sleep(1)
        ret = self.__execStub("stop")
        self.assertEqual(ret.rc, 0)
        ret = self.__interface.sudo("test -f ~/.dockerEE/test_service_service_daemon.check", True)
        self.assertNotEqual(ret.rc, 0)
    ## test ServiceDaemon._getInstance(self)
    # @param self The object pointer
    def testGetInstance(self):
        self.__execStub("start /tmp/env.yml")
        time.sleep(1)
        service = TestService()
        self.assertEqual(service._getInstance().getCount(), 0)
        self.__execStub("stop")
    ## test "python service.py status"
    # @param self The object pointer
    def testStatus(self):
        self.__execStub("start /tmp/env.yml")
        time.sleep(1)
        ret = self.__execStub("status")
        self.assertIn("counter = 0", ret.stdout)
        self.__execStub("stop")
    ## test "python service.py reload"
    # @param self The object pointer
    def testReload(self):
        self.__execStub("start /tmp/env.yml")
        time.sleep(1)
        ret = self.__execStub("reload")
        time.sleep(1)
        ret = self.__execStub("status")
        self.assertIn("counter = 1", ret.stdout)
        self.__execStub("stop")

if __name__ == "__main__":
    unittest.main()
