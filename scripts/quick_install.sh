#!/bin/bash
sudo pip uninstall reqwise -y
# There is no way at the moment to install python dnf module without actually using dnf/yum
sudo dnf install -y python-dnf koji
sudo pip install .
