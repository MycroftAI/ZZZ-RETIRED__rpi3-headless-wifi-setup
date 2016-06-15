#wifi-setup
This project aims to create a web interface, similar to a router setup page, for connecting a Raspberry Pi 3 to a wireless network.

Development Dependencies:
  - virtualenv
  - virtualenvwrapper
  - python-dev

  Debian / Ubuntu / Raspbian:  $  sudo apt-get install virtualenv virtualenvwrapper python-dev

Installation:
  - clone this project into your working directory
  - $ cd ./wifi-setup
  - $ ./setup.sh (creates virtualenv in ~/.virtualenv/wifi-setup

Enter Development Envoronment:
  - $ source ~/.virtualenv/wifi-setup/bin/activate

Configuration File Locations
  - ./configuration/default.ini
  - ./hostapd-shell/config  # System configuration files which are manipulated by hostapd-shell scripts (hostapd, dnsmasq, iptables)
  - ./wifi-setup/web-app/srv/templates/base.html # Base template for index.html. Includes inline jquery.
  - ./wifi-setup/web-app/srv/templates/index.html # Extends base.html. Generates content with tornado.io templating.

