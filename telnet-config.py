import telnetlib
import time

TFTP_SERVER = "10.100.100.8"

SWITCHES = [
    ("10.100.100.2", 32769),
    ("10.100.100.2", 32772),
    ("10.100.100.2", 32774),
    ("10.100.100.2", 32775),
]

def send_multiple_enters(tn, count=2):
    for _ in range(count):
        tn.write(b"\n")
        time.sleep(1)

def initial_configuration(ip, port):
    try:
        print(f"Connecting to {ip}:{port} for initial configuration")
        tn = telnetlib.Telnet(ip, port, timeout=10)
        
        send_multiple_enters(tn, count=3)
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
        print(f"Initial configuration completed on {ip}:{port}")
    except Exception as e:
        print(f"Failed to perform initial configuration on {ip}:{port}. Error: {e}")

def tftp_configuration(ip, port):
    try:
        print(f"Connecting to {ip}:{port} for TFTP configuration")
        tn = telnetlib.Telnet(ip, port, timeout=10)
        
        send_multiple_enters(tn, count=3)
        tn.write(b"en\n")
        time.sleep(1)
        tn.write(f"copy tftp://{TFTP_SERVER}/startup-config running-config\n".encode('ascii'))
        time.sleep(1)
        tn.write(b"\n")  # Confirm the copy with Enter
        time.sleep(1)
        tn.write(b"exit\n")
        tn.close()
        print(f"TFTP configuration completed on {ip}:{port}")
    except Exception as e:
        print(f"Failed to perform TFTP configuration on {ip}:{port}. Error: {e}")

# Step 1: Initial configuration on all switches
for ip, port in SWITCHES:
    initial_configuration(ip, port)

# Step 2: TFTP configuration on all switches
for ip, port in SWITCHES:
    tftp_configuration(ip, port)
