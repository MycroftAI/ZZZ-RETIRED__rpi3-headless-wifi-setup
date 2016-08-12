import time
from bashThreadHandling import bash_command

class dnsmasqTools():
    def __init__(self):
        self.name = "name"
    def dnsmasqServiceStart(self):
        results = bash_command(['systemctl', 'start', 'dnsmasq.service'])
        return results

    def dnsmasqServiceStop(self):
        results = bash_command(['systemctl', 'stop', 'dnsmasq.service'])
        return results

    def dnsmasqServiceStatus(self):
        results = bash_command(['systemctl', 'status', 'dnsmasq.service'])
        return results
    def dnsmasqCli(self):
        results = bash_command(['dnsmasq', '-d', '--interface=uap0', '--dhcp-range=uap0,172.24.1.10,172.24.1.20,255.255.255.0'])
        return results

def main():
    DNS = dnsmasqTools()
    print DNS.dnsmasqServiceStart()
    print DNS.dnsmasqServiceStatus()['stdout'].strip()
    time.sleep(5)
    print DNS.dnsmasqServiceStop()
    print DNS.dnsmasqServiceStatus()['stdout'].strip()
    time.sleep(5)
    print DNS.dnsmasqCli()


if __name__ == "__main__":
    main()
