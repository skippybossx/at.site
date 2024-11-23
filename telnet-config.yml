import telnetlib
import time
from configparser import ConfigParser

TFTP_SERVER = "10.100.100.8"
INVENTORY_FILE = "inventory.ini"

def parse_inventory(file):
    config = ConfigParser()
    config.read(file)
    switches = []
    for switch in config['switches']:
        ip = config['switches'][switch].split()[0].split('=')[1]
        port = config['switches'][switch].split()[1].split('=')[1]
        switches.append((ip, int(port)))
    return switches

def configure_switch(ip, port):
    tn = telnetlib.Telnet(ip, port, timeout=10)
    tn.write(b"\n")
    time.sleep(1)
    tn.write(b"en\n")
    time.sleep(1)
    tn.write(b"conf t\n")
    time.sleep(1)
    tn.write(b"int vlan1\n")
    time.sleep(1)
    tn.write(b"ip address dhcp\n")
    time.sleep(1)
    tn.write(b"no shut\n")
    time.sleep(1)
    tn.write(b"end\n")
    time.sleep(1)
    tn.write(b"exit\n")
    tn.close()
    time.sleep(30)
    tn = telnetlib.Telnet(ip, port, timeout=10)
    tn.write(b"\n")
    time.sleep(1)
    tn.write(b"en\n")
    time.sleep(1)
    tn.write(f"copy tftp://{TFTP_SERVER}/startup-config running-config\n".encode('ascii'))
    time.sleep(1)
    tn.write(b"exit\n")
    tn.close()

switches = parse_inventory(INVENTORY_FILE)
for ip, port in switches:
    configure_switch(ip, port)
