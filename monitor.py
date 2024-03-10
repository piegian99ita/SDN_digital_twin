import requests
import time
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSKernelSwitch, RemoteController
from mininet.link import TCLink
from mininet.cli import CLI

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
        
    

topos = {"networkslicingtopo": (lambda: NetworkTopo())}

def create_network(hosts,switches,links):
    print("\nCreate new network")
    topo = NetworkTopo(hosts,switches,links)
    net = Mininet(
        topo=topo,
        switch=OVSKernelSwitch,
        build=False,
        autoSetMacs=True,
        autoStaticArp=True,
        link=TCLink,
    )
    net.build()
    net.start()
    CLI(net)
    net.stop()

















# Esempio di utilizzo delle funzioni per ottenere le informazioni sulla topologia
if __name__ == "__main__":
    while True:
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
        
        #create_network(new_hosts,new_switches,new_links)
               
        time.sleep(10) 
