import telnetlib
import time

TFTP_SERVER = "10.100.100.8"

SWITCHES = [
    ("10.100.100.2", 32769),
    ("10.100.100.2", 32772),
    ("10.100.100.2", 32774),
    ("10.100.100.2", 32775),
]

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
        print(f"Copied configuration on {ip}:{port}")
    except Exception as e:
        print(f"Failed to configure switch {ip}:{port}. Error: {e}")

for ip, port in SWITCHES:
    configure_switch(ip, port)
