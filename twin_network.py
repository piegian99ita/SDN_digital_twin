import requests
import time
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSKernelSwitch, RemoteController
from mininet.link import TCLink
from mininet.cli import CLI
import os
import time
import threading
import subprocess
from scapy.all import *
import multiprocessing

links_by_definition = None


#questo script serve per definire la topologia della rete ricevendo dal controller queste informazioni 


# Definizione degli endpoint dell'API REST
BASE_URL = 'http://127.0.0.1:8080/v1.0/topology'
SWITCHES_ENDPOINT = '/switches'
LINKS_ENDPOINT = '/links'
HOSTS_ENDPOINT = '/hosts'

# Funzione per ottenere informazioni su tutti gli switch nella topologia
def get_switches():
    response = requests.get(BASE_URL + SWITCHES_ENDPOINT)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Funzione per ottenere informazioni su tutti i collegamenti nella topologia
def get_links():
    response = requests.get(BASE_URL + LINKS_ENDPOINT)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Funzione per ottenere informazioni su tutti gli host nella topologia
def get_hosts():
    response = requests.get(BASE_URL + HOSTS_ENDPOINT)
    if response.status_code == 200:
        return response.json()
    else:   
        return None



class NetworkTopo(Topo):
    def __init__(self,hosts,switches,links):
        # Initialize topology
        Topo.__init__(self)

        # Create template host, switch, and link
        host_config = dict(inNamespace=True)
        
        link_config = dict(bw=1)
        for switch in switches:
            sconfig = {"dpid": "%016x" % (int(switch['dpid'], 16)+10) }
            self.addSwitch(switch['name']+"_twin", **sconfig)

        # Create host nodes
        for i in hosts:
            self.addHost(i+"_twin" , **host_config)

        
        # Add switch links
        for link in links:
            self.addLink(link['first']+"_twin",link['second']+"_twin",**link_config)
        
    

topos = {"digital_twin_topo": (lambda: NetworkTopo())}





def host_write(host,index):
    while not host.shell or host.waiting:
        time.sleep(1)
    
    
    
    name=str(host).replace("_twin","")
    #print(name)
    
    file_name="./capture/capture_"+name+"_"+str(index)+".pcap"
    file_name2="./capture/capture_"+name+"_"+str(index+1)+".pcap"
        
    #print("Entered before")
    

    while (not os.path.exists(file_name2)):
        time.sleep(1)

    packets = rdpcap(file_name)
    
    
    filtered_packets = [packet for packet in packets if (packet.haslayer(IP) and packet[IP].src == host.IP() and not(packet.haslayer(ICMP))) or(packet.haslayer(IP) and packet[IP].src == host.IP() and packet.haslayer(ICMP) and packet[ICMP].type == 8)  ]
    if filtered_packets:
        print("-------------packets sent-----------")
        wrpcap(file_name, filtered_packets)
    

    #time.sleep(4)
    #print("tcpreplay --intf1="+ str(host.intfNames()[0]) +" " + file_name)
    #host.cmd("tcprewrite --infile="+ file_name +" --outfile=" + file_name+ " --fixcsum" )
    host.cmd("tcpreplay --intf1="+ str(host.intfNames()[0]) +" " + file_name +" &")
    #print("--- PACKETS SENT ---")
    
    subprocess.run(['rm', '-f', file_name])
    
    
    
    
        




def network_write(net):
      
    file_path="start.txt"
    with open(file_path, 'w'):
        pass
    
    
    hosts=net.hosts
    thread_list=[] 
    i=0  
    cont=0
    index=0
    while True: 
        for host in hosts:
            thread_list.append(threading.Thread(target=host_write, args=(host,index,)))
            thread_list[i].start()
            i+=1
            #print(host)
        
        for threads in thread_list:
            threads.join() 
        if cont%3==0:
            check_links()
        cont+=1%3
        index+=1
    




def check_links():
    global links_by_definition

    
        
    links=get_links()
    for link in links_by_definition:
        
        node1 = link.intf1.node.name
        node2 = link.intf2.node.name
        
        if not (link.intf1.node.name.startswith('s') and link.intf2.node.name.startswith('s')):
            continue
        
        
        flag_exists=False
    
        for current_link in links:
            
            if node1.split('_')[0]==current_link["src"]["name"].split('-')[0] and node2.split('_')[0]==current_link["dst"]["name"].split('-')[0]:
                flag_exists=True
                link.intf1.ifconfig('up')
                link.intf2.ifconfig('up')
                
        
        if not flag_exists:
            link.intf1.ifconfig('down')
            link.intf2.ifconfig('down')





def create_network(hosts,switches,links):
    global links_by_definition
    print("\nCreate new network")
    digital_topo = NetworkTopo(hosts,switches,links)
    net2 = Mininet(
        topo=digital_topo,
        switch=OVSKernelSwitch,
        build=False,
        autoSetMacs=True,
        autoStaticArp=True,
        link=TCLink,
        #controller=None,
    )
    controller = RemoteController("c1", ip="127.0.0.1", port=5544)
    net2.addController(controller)
    net2.build()
    net2.start()
    links_by_definition=net2.links
    thread=threading.Thread(target=network_write, args=(net2,))
    thread.start()

    #check_link=threading.Thread(target=check_links, args=(net2,))

    # process = multiprocessing.Process(target=check_links, args=(net2,))
    # process.daemon = True
    # process.start()
    #check_link.start()
    CLI(net2)
    net2.stop()











# Esempio di utilizzo delle funzioni per ottenere le informazioni sulla topologia
if __name__ == "__main__":

    print("\n\nSTART MONITORING!")
    new_links=[]
    new_hosts=[]
    new_switches=[]
    
    
    #We add the switches to our new network
    switches = get_switches()
    
    if switches:
        for switch in switches:
            dicto={"name":"s%d" % int(switch['dpid']), "dpid":"%016x" % int(switch['dpid'])}
            new_switches.append(dicto)
                        
    
    
    #We get the links from the hosts
    hosts=get_hosts()
    
    if hosts:
        for host in hosts:
            mac_parts=host['mac'].split(":")
            first=0
            for part in mac_parts:
                first = (first << 8) + int(part, 16)
            
            new_hosts.append("h%d" % first)
            
            dicto={"first":"h%d" % first, "second":"s%d" % int(host['port']['dpid'])}
            new_links.append(dicto)
            #print(str(index)+". [Mac:"+host['mac']+"  port:{"+"dpid:'"+host['port']['dpid']+"' name:"+host['port']['name']+"]")
    
    
    
    #We get the links from the switches
    links=get_links()
    
    if links:
        for link in links:
                dicto={"first":"s%d" % int(link['src']['dpid']), "second":"s%d" % int(link['dst']['dpid'])}
                new_links.append(dicto)
    
            
    
    #We check for duplicates: 
    # Such as: [{first:"s1", second:"s2"},{first:"s2",second:"s1"}] 
    for link in new_links:
        first=link['first']
        second=link['second']
        for index,secLink in enumerate(new_links):
            if secLink['first']==second and secLink['second']==first:
                del new_links[index]
    
    
    #Print all devices and links we see from our network
    if new_hosts:
        print("\nHosts:")
        for host in new_hosts:
            print(host)
    
    if new_switches:
        print("\nSwitches:")
        for switch in new_switches:
            print(switch)
    
    if new_links:
        print("\nLinks:")
        for links in new_links:
            print(links)  
    
    create_network(new_hosts,new_switches,new_links)
            
    

