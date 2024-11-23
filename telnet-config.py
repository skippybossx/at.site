import telnetlib
import time
from configparser import ConfigParser

TFTP_SERVER = "10.100.100.8"
INVENTORY_FILE = "inventory.ini"

def parse_inventory(file):
    config = ConfigParser(allow_no_value=True)
    config.read(file)
    switches = []
    for switch in config['switches']:
        ip = config['switches'][switch].split('ansible_host=')[1].split()[0]
        port = config['switches'][switch].split('ansible_port=')[1].split()[0]
        switches.append((ip, int(port)))
    return switches

def configure_switch(ip, port):
    try:
        print(f"Connecting to {ip}:{port}")
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
        print(f"Configured VLAN1 on {ip}:{port}")

        time.sleep(30)

        print(f"Copying TFTP configuration on {ip}:{port}")
        tn = telnetlib.Telnet(ip, port, timeout=10)
        tn.write(b"\n")
        time.sleep(1)
        tn.write(b"en\n")
        time.sleep(1)
        tn.write(f"copy tftp://{TFTP_SERVER}/startup-config running-config\n".encode('ascii'))
        time.sleep(1)
        tn.write(b"exit\n")
        tn.close()
    except Exception as e:
        print(f"Failed to configure switch {ip}:{port}. Error: {e}")

switches = parse_inventory(INVENTORY_FILE)
for ip, port in switches:
    configure_switch(ip, port)
