#!/usr/bin/python3

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSKernelSwitch, RemoteController
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel, info
from mininet.util import dumpNodeConnections
import os
import time
import threading
import multiprocessing


class NetworkTopo(Topo):
    
    
    def __init__(self):
        # Initialize topology
        Topo.__init__(self)

        # Create template host, switch, and link
        host_config = dict(inNamespace=True)
        
        link_config = dict(bw=1)
        

        for i in range(2):
            sconfig = {"dpid": "%016x" % (i + 1)}
            self.addSwitch("s%d" % (i + 1), **sconfig)

        #self.addLink("s1","s2",**link_config)
        #self.addLink("s2","s3",**link_config)
        # Create host nodes
        for i in range(2):
            self.addHost("h%d" % (i + 1), **host_config)
        

        # Add host links    
    
        self.addLink("h1","s1")
        self.addLink("h2","s2")
        self.addLink("s1","s2")
        #self.addLink("h3","s2")    
        #self.addLink("h4","s3")
        # Add switch links
        
           
        
        
        #self.addLink("h4", "s4", **link_config)

        # # Create switch nodes
        # for i in range(4):
        #     sconfig = {"dpid": "%016x" % (i + 1)}
        #     self.addSwitch("s%d" % (i + 1), **sconfig)

        # # Create host nodes
        # for i in range(6):
        #     self.addHost("h%d" % (i + 1), **host_config)

        
        

        # # Add host links
        # self.addLink("h1", "s1", **host_link_config)
        # self.addLink("h2", "s1", **host_link_config)
        # self.addLink("h3", "s4", **host_link_config)
        # self.addLink("h4", "s4", **host_link_config)
        # self.addLink("h5", "s2", **host_link_config)
        # self.addLink("h6", "s3", **host_link_config)


topos = {"networkslicingtopo": (lambda: NetworkTopo())}








import subprocess

def host_read(host):
    while not host.shell or host.waiting:
        time.sleep(1)
    
    interface=str(host)+'-eth0'
    
    print("Called interface : "+interface)
    index=0
    
    while True:
        file_name="./capture/capture_"+str(host)+"_"+str(index)+".pcap"
        
        send_cmd="timeout 10 tcpdump -i "+interface+" not ether proto 0x88cc and not icmp6 -w "+file_name+" &"
        #Come mettere in background il processo
        host.cmd(send_cmd)
        
        time.sleep(10)
        
        index=index+1

def network_read_write(net):
    hosts=net.hosts
    file_path="start.txt"
    subprocess.run(['rm', '-f', file_path])
    subprocess.run('rm -f ./capture/*', shell=True)
    #subprocess.run(['rm','-f',"./capture/*"])


    
    print("Wait")
    file_path="start.txt"
    
    while not os.path.isfile(file_path):
        time.sleep(2)
        
    print("Finished waiting")
    thread_list=[] 
    i=0
    for host in hosts:
        thread_list.append(threading.Thread(target=host_read, args=(host,)))
        #thread_list[i].daemon = True
        thread_list[i].start()
        i+=1
        print(host)
    
    for threads in thread_list:
        threads.join() 
        
        
        

if __name__ == "__main__":
    topo = NetworkTopo()
    net = Mininet(
        topo=topo,
        switch=OVSKernelSwitch,
        build=False,
        autoSetMacs=True,
        autoStaticArp=True,
        link=TCLink,
    )
    controller = RemoteController("c1", ip="127.0.0.1", port=6633)
    net.addController(controller)
    net.build()
    net.start()
    # Connect to the custom controller
    net.controllers[0].start()
    
    # Set MAC address of the controller
    custom_controller = net.controllers[0]
    custom_controller.mac_address = "11:00:00:00:00:01"

    # Wait for network to stabilize
    net.waitConnected()
    
    
    #thread=threading.Thread(target=network_read_write, args=(net,))
    #thread.start()
    process = multiprocessing.Process(target=network_read_write, args=(net,))
    process.daemon = True
    process.start()
    
    CLI(net)
    net.stop()


    #thread.join()
    
