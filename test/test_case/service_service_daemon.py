import sys
sys.path.append("../../")

import unittest

from dockerEE.remote import RemoteInterfaceImpl

from service_test_utils import ServiceTestUtils
from service_service_daemon_stub import TestService

## TestServerDaemon
#
# The test case for ServiceDaemon
class TestServiceDaemon(unittest.TestCase):
    ## init test case
    # @param self The object pointer
    def setUp(self):
        arg = {"host": "localhost", "user": "vagrant", "password": "vagrant"}
        ## service test utils
        self.__service = ServiceTestUtils("python /vagrant/test/test_case/service_service_daemon_stub.py", **arg)
        ## remote interface
        self.__interface = RemoteInterfaceImpl(**arg)
        ## starting file name
        self.__filename = "/tmp/service_service_daemon"
        open(self.__filename, "w")
    ## test "python service.py start/stop"
    # @param self The object pointer
    def testStartStop(self):
        ret = self.__service.start(self.__filename, 10)
        self.assertEqual(ret.rc, 0)
        ret = self.__interface.sudo("test -f ~/.dockerEE/test_service_service_daemon.check", True)
        self.assertEqual(ret.rc, 0)
        ret = self.__service.stop(10)
        self.assertEqual(ret.rc, 0)
        ret = self.__interface.sudo("test -f ~/.dockerEE/test_service_service_daemon.check", True)
        self.assertNotEqual(ret.rc, 0)
    ## test ServiceDaemon._getInstance(self)
    # @param self The object pointer
    def testGetInstance(self):
        self.__service.start(self.__filename, 10)
        service = TestService()
        self.assertEqual(service._getInstance().getCount(), 0)
        self.__service.stop(10)
    ## test "python service.py status"
    # @param self The object pointer
    def testStatus(self):
        self.__service.start(self.__filename, 10)
        ret = self.__service.status()
        self.assertIn("counter = 0", ret.stdout)
        self.__service.stop(10)
    ## test "python service.py reload"
    # @param self The object pointer
    def testReload(self):
        self.__service.start(self.__filename, 10)
        self.__service.reload()
        ret = self.__service.status()
        self.assertIn("counter = 1", ret.stdout)
        self.__service.stop(10)

if __name__ == "__main__":
    unittest.main()
