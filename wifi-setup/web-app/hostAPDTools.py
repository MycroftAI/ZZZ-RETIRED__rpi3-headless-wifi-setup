import time
from bashThreadHandling import bash_command

class hostAPServerTools():
    def __init__(self):
        self.name = "name"
    def hostAPDStart(self):
        results = bash_command(['systemctl', 'start', 'hostapd.service'])
        return results

    def hostAPDStop(self):
        results = bash_command(['systemctl', 'stop', 'hostapd.service'])
        return results

    def hostAPDStatus(self):
        results = bash_command(['systemctl', 'status', 'hostapd.service'])
        return results

def main():
    HostAP = hostAPServerTools()
    print HostAP.hostAPDStart()
    time.sleep(10)

    print HostAP.hostAPDStatus()['stdout'].strip()
    print HostAP.hostAPDStop()

    print HostAP.hostAPDStatus()['stdout'].strip()


if __name__ == "__main__":
    main()
