
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Controller, RemoteController
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.clean import cleanup
from time import sleep
import os
import base64
import signal
import json
# Stop warnings from scapy.
from warnings import filterwarnings
filterwarnings("ignore")
from scapy.all import *


def load_pcap_data(pcap,host_list):
  for pkt in pcap:
    for host in host_list:
      if pkt[IP].src==host.IP():
        host.cmd("python3 -c \"import base64; from scapy.sendrecv import sendp; sendp(base64.b64decode(" +  str(pkt) + "), iface='" + h1.intfNames()[0] + "')\"")



