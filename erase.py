import telnetlib
import time

SWITCHES = [
    ("10.100.100.2", 32769),
    ("10.100.100.2", 32772),
    ("10.100.100.2", 32774),
    ("10.100.100.2", 32775),
]

def clear_switch(ip, port):
    try:
        print(f"Connecting to {ip}:{port}")
        tn = telnetlib.Telnet(ip, port, timeout=10)
        
        tn.write(b"\n")
        time.sleep(1)
        tn.write(b"en\n")
        time.sleep(1)
        tn.write(b"write erase\n")
        time.sleep(2)  # Wait for the confirmation prompt
        tn.write(b"y\n")  # Confirm the write erase
        time.sleep(1)
        print(f"Write erase completed for {ip}:{port}")
        
        tn.write(b"reload\n")
        time.sleep(2)  # Wait for the confirmation prompt
        tn.write(b"y\n")  # Confirm the reload
        time.sleep(1)
        tn.close()
        print(f"Reload initiated for {ip}:{port}")
    except Exception as e:
        print(f"Failed to clear switch {ip}:{port}. Error: {e}")

for ip, port in SWITCHES:
    clear_switch(ip, port)
