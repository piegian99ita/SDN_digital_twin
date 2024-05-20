#!/usr/bin/python3

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSKernelSwitch, RemoteController
from mininet.cli import CLI
from mininet.link import TCLink
from time import sleep
import threading




class NetworkTopo(Topo):
    def __init__(self):
        # Initialize topology
        Topo.__init__(self)

        # Create template host, switch, and link
        host_config = dict(inNamespace=True)
        
        link_config = dict(bw=10)
        

        for i in range(4):
            sconfig = {"dpid": "%016x" % (i + 1)}
            self.addSwitch("s%d" % (i + 1), **sconfig)

        # Create host nodes
        for i in range(3):
            self.addHost("h%d" % (i + 1), **host_config)

        
        # Add switch links
        self.addLink("s1", "s2", **link_config)
        self.addLink("s2", "s4", **link_config)
        self.addLink("s2", "s3", **link_config)
        
        # Add host links
        self.addLink("h1", "s1", **link_config)
        self.addLink("h2", "s3", **link_config)
        self.addLink("h3", "s4", **link_config)
        

        


topos = {"networkslicingtopo": (lambda: NetworkTopo())}


def send_pcap_data(host_list,events):
  sleep(15)
  for delay in events:
      delay.wait()
  print("----------------SENDING PACKETS-------------")
  for host in host_list:
    print("--PROVA--     "+ str(host))
    host.cmd("tcprewrite --infile="+ str(host) +".pcap --outfile=" + str(host) + "_final.pcap --fixcsum" )
    print("----------------SCRITTO FILE MODIFICATO----------------")
    host.cmd("tcpreplay --intf1="+ str(host.intfNames()[0]) +" " + str(host) +  "_final.pcap")
    print("----------------PACCHETTI INVIATI----------------")
  
def generate_traffic(host,events):  
    print(host)
    while not host.shell or host.waiting:
        sleep(1)
    
    if str(host)=="h1":
        print("1-h1")
        events[0].wait()
        #sleep(1)
        host.cmd("iperf -c 10.0.0.2 -u -b 10M -t 10")  

    elif str(host)=="h2":
        print("1-h2")
        events[1].wait()
        #sleep(1)
        host.cmd("iperf -c 10.0.0.3 -u -b 10M -t 10")

    elif str(host)=="h3":
        print("1-h3")
        events[2].wait()
        #sleep(1)
        host.cmd("iperf -c 10.0.0.1 -u -b 10M -t 10")
    else:
        print("ERRORE NELLA LETTURA DEI FILE!11111111")

def read_traffic(host,events): 
    print(host)
    while not host.shell or host.waiting:
        sleep(1)  
    if str(host)=="h1":
        print("2-h1")
        events[2].set()
        host.cmd("tcpdump -i h1-eth0 not ether proto 0x88cc and not icmp6 -w h1.pcap  ")
        #events[2].set()
          
    elif str(host)=="h2":
        print("2-h2")
        events[0].set()
        host.cmd("timeout 15 tcpdump -i h2-eth0 not ether proto 0x88cc and not icmp6 -w h2.pcap")
        #events[0].set()
        
    elif str(host)=="h3":
        print("2-h3")
        events[1].set()
        host.cmd("tcpdump -i h3-eth0 not ether proto 0x88cc and not icmp6 -w h3.pcap -W 1 15 ")
        #events[1].set()
    else:
        print("ERRORE NELLA LETTURA DEI FILE!2222222")
    
   

        

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
    sleep(5)
    

    #create the hosts list 
    hosts_list=[]
    
    events=[threading.Event(),threading.Event(),threading.Event()]
    
    


    for node in net.hosts:
        # Check if the node is a host
        if 'h' in node.name:
            # Append the host to the list
            hosts_list.append(node)
    

    #create the traffic by using a function 
   
    
    read_threads=threading.Thread(target=read_traffic,args=(hosts_list[1],events,))
    traffic_threads=threading.Thread(target=generate_traffic,args=(hosts_list[0],events,))
    
    
    print("start ")
    read_threads.start()
    traffic_threads.start()
    
    sleep(17)
    

    
    print("join " )
    read_threads.join()
    traffic_threads.join()
   
   
    

    
    
    #start a new thread while we start the CLI to send packets to the hosts this function will be put in the monitor script 
    #send_thread = threading.Thread(target=send_pcap_data, args=(hosts_list,events,))
    #send_thread.start()

    #start the CLI while the sending packets thread is ongoing
    CLI(net)

   
    
    #send_thread.join()
    net.stop()


