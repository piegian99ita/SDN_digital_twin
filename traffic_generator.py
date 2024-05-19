import subprocess
import socket
import sys
import re

def get_local_ip():
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # Connect to a remote host (Google DNS) to get the local IP address
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
    except:
        local_ip = '127.0.0.1'  # Default to loopback address if unable to connect

    finally:
        s.close()

    return local_ip

def discover_hosts():
    # Run nmap to discover active hosts within the network
    nmap_command = ['nmap', '-sn', get_local_ip()[:-1] + '0/24']
    nmap_output = subprocess.check_output(nmap_command, universal_newlines=True)

    # Extract IP addresses of discovered hosts from nmap output
    host_ips = re.findall(r'(\d+\.\d+\.\d+\.\d+)', nmap_output)

    return host_ips

def generate_traffic(client_ip):
    # Start ping command to generate traffic from this host to the client
    ping_command = ['ping', '-c', '10', client_ip]  # Sends 10 ping packets
    subprocess.run(ping_command)

if __name__ == "__main__":
    # Get the local IP address
    local_ip = get_local_ip()

    # Discover active hosts within the network
    host_ips = discover_hosts()

    # Check if any hosts were discovered
    if not host_ips:
        print("No hosts found in the network.")
        sys.exit(1)

    # Iterate through each discovered host and generate traffic
    while True:
    	for client_ip in host_ips:
        	# Skip if client_ip is the same as local_ip
        	if client_ip == local_ip:
            		continue
        	# Generate traffic from this host to the client
        	generate_traffic(client_ip)
