ReqWise
=======

Requirements analysis for Python projects on RHEL/Fedora/CentOS

Install
-------

To install reqwise on your system, run the following command:

    sudo pip install .

### Configuration

Can be set in your current working directory (reqwise.conf) or
in '/etc/reqwise/reqwise.conf'

The configuration file consists of sources. Source is where reqwise
will look for your requirement

An example for configration file:

    [copr]
    el7-rhos9-test-deps
    el7-rhos10-test-deps

    [koji]
    disabled=True

    [yum]
    repos=my_repo,another_repo


Supported Sources
-----------------

None ATM :D


Examples
--------

To analyse the default requirements files in your current directory:

    reqwise
