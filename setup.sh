#!/bin/bash

set -Ee
TOP=$(cd $(dirname $0) && pwd -L)
VIRTUALENV_ROOT=${VIRTUALENV_ROOT:-"${HOME}/.virtualenvs/wifi-setup"}

if [ ! -d ${VIRTUALENV_ROOT} ]; then
  mkdir -p $(dirname ${VIRTUALENV_ROOT})
  virtualenv ${VIRTUALENV_ROOT}
fi
source ${VIRTUALENV_ROOT}/bin/activate
cd ${TOP}

easy_install pip==7.1.2 # force version of pip
pip install -r requirements.txt  # install reqs

