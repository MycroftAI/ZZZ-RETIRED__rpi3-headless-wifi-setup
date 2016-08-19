#!/usr/bin/env bash

# set working path TOP
TOP=$(cd $(dirname $0) && pwd -L)
# set virtualenv name and location
VIRTUALENV_ROOT=${VIRTUALENV_ROOT:-"${HOME}/.virtualenvs/wifi-setup"}

# case statement for script input options
case $1 in
    "main") SCRIPT=${TOP}/wifi-setup/main.py ;;  # run the main program
	*) echo "Usage: start.sh [main]"; exit ;;
esac

echo "Starting $@"

shift

# activate virtualenv
source ${VIRTUALENV_ROOT}/bin/activate

# set PYTHONPATH environment variable and run selected program
PYTHONPATH=${TOP} python ${SCRIPT} $@
