import requests
import time
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSKernelSwitch, RemoteController
from mininet.link import TCLink
from mininet.cli import CLI
import subprocess


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

def create_network(hosts, switches, links):
    print("\nCreate new digital network")
    net2 = Mininet(
        topo=None,
        switch=OVSKernelSwitch,
        build=False,
        autoSetMacs=True,
        autoStaticArp=True,
        link=TCLink,
    )
    controller = RemoteController("c1", ip="127.0.0.1", port=5544)
    net2.addController(controller)
    net2.controllers[0].start()  # Start the controller before building the network

    digital_topo = NetworkTopo(hosts, switches, links)
    net2.buildFromTopo(digital_topo)
    net2.start()

    return net2
    # CLI(net2)
    # net2.stop()
    # return net2

















# Esempio di utilizzo delle funzioni per ottenere le informazioni sulla topologia
if __name__ == "__main__":
    i=0
    old_links=[]
    old_hosts=[]
    old_switches=[]
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
        if i==0:
            print(i)
            net2=create_network(new_hosts,new_switches,new_links)
        #CLI(net2)
        #net2.stop()
        else:
            
            
            host_config = dict(inNamespace=True)
            link_config = dict(bw=1)
    
            print(old_hosts)
            print(new_hosts)

            # host changes
            added_hosts = [dict for dict in new_hosts if dict not in old_hosts]
            removed_hosts = [dict for dict in old_hosts if dict not in new_hosts]

            # switch changes
            added_switches=[dict for dict in new_switches if dict not in old_switches]
            removed_switches=[dict for dict in old_switches if dict not in new_switches]

            # links changes
            added_links = [dict for dict in new_links if dict not in old_links]
            removed_links = [dict for dict in old_links if dict not in new_links]

            # if added_hosts:
            #     print("links created")
            #     for host in added_hosts:
            #         net2.addHost(host + "_twin",**host_config)
            # if removed_hosts:
            #     print("links removed1")
            #     for host in removed_hosts:
            #         net2.removeHost(host + "_twin")

            
            
            # if added_switches:
            #     print("links created2")
            #     for switch in added_switches:
            #         sconfig = {"dpid": "%016x" % (int(switch['dpid'], 16)+10) }
            #         net2.addSwitch(switch['name']+"_twin", **sconfig)
            # if removed_switches:
            #     print("links removed2")
            #     for switch in removed_switches:
            #         net2.removeSwitch(switch['name']+"_twin")
            
            # print("build")
            # net2.configHosts()
            # net2.configSwitches()
            # print("post build")

            
            # if added_links:
            #     for link in added_links:
            #         print("links created3")
            #         net2.addLink(link['first']+"_twin",link['second']+"_twin",**link_config)
            # if removed_links:
            #     print("links removed3")
            #     for link in links:
            #         net2.configLinkStatus(link['first']+"_twin",link['second']+"_twin",'down')
            
            #remove old links
            for link in removed_links:
                net2.delLink(link['first']+"_twin", link['second']+"_twin")

            # Remove old hosts and switches
            for host in removed_hosts:
                net2.get(host+"_twin").stop()
                net2.get(host+"_twin").terminate()
            for switch in removed_switches:
                net2.get(switch['name']+"_twin").stop()
                net2.get(switch['name']+"_twin").terminate()

            # Add new hosts and switches
            for host in added_hosts:
                net2.addHost(host+"_twin")
            for switch in added_switches:
                sconfig = {"dpid": "%016x" % (int(switch['dpid'], 16)+10)}
                net2.addSwitch(switch['name']+"_twin", **sconfig)

            # Add new links
            for link in added_links:
                net2.addLink(link['first']+"_twin", link['second']+"_twin")

            
            p
            net2.configHosts()
            
          


        old_links=new_links
        old_hosts=new_hosts
        old_switches=new_switches
        i+=1
        
        net2.controllers[0].stop()
        
        net2.controllers[0].start()
        CLI(net2)
        # net2.stop()
        # time.sleep(10) 
