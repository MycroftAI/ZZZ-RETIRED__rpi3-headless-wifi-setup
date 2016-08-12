import time
from bashThreadHandling import bash_command
import pyric
from pyric import


class wpaManipulationTools():
    def __init__(self):
        self.name = "name"
    def getInterfaces(self):
        try:
            results = pyw.interfaces()
            return results
        except pyric.error as e:
            print e
            return e

    def getWInterfaces(self):
        try:
            results = pyw.winterfaces()
            return results
        except pyric.error as e:
            print e
            return e

    def isWInterface(self, iface):
        try:
            results = pyw.iswinterface(iface)
        except pyric.error as e:
            print e
            return e
            

class wpaClientTools():
    def __init__(self):
        self.name = "name"
    def wpa_cli_flush(self):
        results = bash_command(['wpa_cli','flush'])
        return results

    def wpa_cli_scan(self,iface):
        bash_command(['wpa_cli', '-i', iface, 'scan'])
        results = bash_command(['wpa_cli','scan_results'])
        return results

    def wpa_cli_status(self,iface):
        status = bash_command(['wpa_cli', '-i', iface, 'status'])
        status = status['stdout'].split('\n', 13)
        results = {
            "bssid": status[0].split("=", 1)[1],
            "freq": status[1].split("=", 1)[1],
            "ssid": status[2].split("=", 1)[1],
            "id": status[3].split("=", 1)[1],
            "mode": status[4].split("=", 1)[1],
            "pairwise_cipher": status[5].split("=", 1)[1],
            "group_cipher": status[6].split("=", 1)[1],
            "key_mgmt": status[7].split("=", 1)[1],
            "wpa_state": status[8].split("=", 1)[1],
            "ip_address": status[9].split("=", 1)[1],
            "p2p_device_address": status[10].split("=", 1)[1],
            "address": status[11].split("=", 1)[1],
            "uuid": status[12].split("=", 1)[1]
        }
        return results

    def wpa_cli_loglevel_debug(self,iface):
        results = bash_command(['wpa_cli', '-i', iface, 'log_level', 'debug'])
        return results
    def wpa_cli_add_network(self,iface):
        results = bash_command(['wpa_cli', '-i', iface, 'add_network'])
        return results
    def wpa_cli_set_network(self,iface, network_id, network_var, network_var_value):
        results = bash_command(['wpa_cli', '-i', iface, 'set_network', network_id, network_var, network_var_value])
        return results
    def wpa_cli_enable_network(self,iface, network_id):
        results = bash_command(['wpa_cli', '-i', iface, 'enable', network_id])
        return results
    def wpa_cli_disable_network(self, network_id):
        results = bash_command(['wpa_cli', '-i', iface, 'disable', network_id])
        return results
    def wpa_save_network(self, network_id):
        results = bash_command(['wpa_cli', 'save', network_id])
        return results

def main():
    WiFi = wpaManipulationTools()
    interfaces = WiFi.getInterfaces()
    winterfaces = WiFi.getWInterfaces()
    print winterfaces
    for iface in winterfaces:
        print WiFi.isWInterface(iface)




if __name__ == "__main__":
    main()
