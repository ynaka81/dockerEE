import os
import sys
from dockerEE.service import EnvironmentEmulationService

if __name__ == "__main__":
    # change 2nd argument to abspath
    if len(sys.argv) >= 3 and os.path.isfile(sys.argv[2]):
        sys.argv[2] = os.path.abspath(sys.argv[2])
    # service action
    service = EnvironmentEmulationService('localhost', 'vagrant', 'vagrant')
    service.action()
