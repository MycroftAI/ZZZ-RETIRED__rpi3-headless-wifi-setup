#!/usr/bin/env bash

# install debian dependencies
sudo apt-get update && apt-get install dnsmasq hostapd virtualenv virtualenvwrapper python-dev -y

# exit on any error
set -Ee

# set working path TOP
TOP=$(cd $(dirname $0) && pwd -L)
# set virtualenv name and location
VIRTUALENV_ROOT=${VIRTUALENV_ROOT:-"${HOME}/.virtualenvs/wifi-setup"}

# create virtualenv for user if it does not exist
if [ ! -d ${VIRTUALENV_ROOT} ]; then
  mkdir -p $(dirname ${VIRTUALENV_ROOT})
  virtualenv ${VIRTUALENV_ROOT}
fi

# activate virtualenv
source ${VIRTUALENV_ROOT}/bin/activate
cd ${TOP}

# force pip version
easy_install pip==7.1.2

# install python dependencies with pip into virtualenv
pip install -r requirements.txt

