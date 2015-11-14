dockerEE
========

![dockerEE](https://github.com/ynaka81/dockerEE/wiki/images/dockerEE.png)

Description
-----------
The python wrapper of constructing the emulation environment by docker.
It will make you free from troublesome environment use planning or resource planning to do something on production environment,
dockerEE only needs typical 1VM(4GB mem) to emulate dozens of servers and switches.

dockerEE has service interfaces to construct/destruct the emulation environment from simple YAML file.
So it is simple to use.

Requirement
-----------
dockerEE depends on the following packages.
- [docker](https://github.com/docker/docker)
- [pipework](https://github.com/jpetazzo/pipework)
- [python-daemon](https://github.com/arnaudsj/python-daemon)
- [Pyro4](https://github.com/irmen/Pyro4)
- [PyYAML](https://github.com/yaml/pyyaml)
- [fabric](https://github.com/fabric/fabric)
- [ipaddress](http://docs.python.jp/3/library/ipaddress.html)

Usage
-----
To start emulation environment defined by demo/hello_dockerEE/env.yml,

    $ python main.py start demo/hello_dockerEE/env.yml

After starting the environment, you can get the status,

    $ python main.py status

           Active: active (running)
         Main PID: 3603

     App Specific: loaded items
    servers
            c1
                    eth0 : 192.168.0.1/24 via 192.168.0.254/24
            c2
                    eth0 : 192.168.0.2/24
                    eth1 : 192.168.1.2/24 via 192.168.1.254/24

When you finish to use the environment, you can stop,

    $ python main.py stop

If you want to initialize the one server (ex. "c1"),

    $ python main.py reload c1

Development status
------------------
The project is now in development.
The development status is below.

- [x] OS
    * [x] start
    * [x] stop
    * [x] status
    * [x] restart
- [ ] network
    * [ ] start
    * [ ] stop
    * [ ] status
    * [ ] restart
- [x] service interface
    * [x] start
    * [x] stop
    * [x] status
    * [x] restart
- [ ] middleware
