#wifi-setup  -- WIP(dangerzone)
This project aims to create a web interface, similar to a router setup page, for connecting a Raspberry Pi 3 to a wireless network.
Beware that this project will manipulate system files and services. Running this software will also require sudo (for now).

Development Dependencies:
  - virtualenv
  - virtualenvwrapper
  - python-dev

  Debian / Ubuntu / Raspbian:  $  sudo apt-get install virtualenv virtualenvwrapper python-dev

Installation:
  - clone this project into your working directory
  - $ `cd ./wifi-setup`
  - $ `sudo ./setup.sh (creates virtualenv in ~/.virtualenv/wifi-setup`  <<-using sudo will create this in the /root directory for now)

Enter Development Environment:
  - $ `source ~/.virtualenv/wifi-setup/bin/activate`

Configuration File Locations:
  - ./configuration/default.ini

Starting the server:
  - `sudo ./start.sh main`
