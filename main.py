# import sys
# sys.path.append('./')
from dockerEE.service import EnvironmentEmulationService

if __name__ == "__main__":
    service = EnvironmentEmulationService('localhost', 'vagrant', 'vagrant')
    service.action()
