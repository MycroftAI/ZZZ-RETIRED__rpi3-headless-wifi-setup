#wifi-setup  -- WIP(dangerzone)
This project aims to create a web interface, similar to a router setup page, for connecting a Raspberry Pi 3 to a wireless network.
Beware that this project will manipulate system files and services. Running this software will also require sudo.

Development Dependencies:
  - virtualenv
  - virtualenvwrapper
  - python-dev

  Debian / Ubuntu / Raspbian:  $  sudo apt-get install virtualenv virtualenvwrapper python-dev

Installation:
  - clone this project into your working directory
  - $ cd ./wifi-setup
  - $ ./setup.sh (creates virtualenv in ~/.virtualenv/wifi-setup

Enter Development Environment:
  - $ source ~/.virtualenv/wifi-setup/bin/activate

Configuration File Locations:
  - ./configuration/default.ini

Starting the server:
  - `./start.sh main`
