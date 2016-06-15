#!/usr/bin/env bash
TOP=$(cd $(dirname $0) && pwd -L)
VIRTUALENV_ROOT=${VIRTUALENV_ROOT:-"${HOME}/.virtualenvs/wifi-setup"}

case $1 in
	"install") SCRIPT=${TOP}./install-deps.sh ;;
	"ap-up") SCRIPT=${TOP} ./ap-up.sh;;
	"ap-down") SCRIPT=${TOP} ./ap-up.sh;;
	*) echo "hostapd portal - Usage: start.sh [ install | ap-up | ap-down ]"; exit ;;
esac

echo "Starting $@"

shift

source ${VIRTUALENV_ROOT}/bin/activate
PYTHONPATH=${TOP} python ${SCRIPT} $@
