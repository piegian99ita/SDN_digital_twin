#!/usr/bin/python3

import time
import threading
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSKernelSwitch, RemoteController
from mininet.cli import CLI
from mininet.link import TCLink

class NetworkTopo(Topo):
    def __init__(self):
        # Initialize topology
        Topo.__init__(self)

        # Create template host, switch, and link
        host_config = dict(inNamespace=True)
        link_config = dict(bw=1)

        # Create switch nodes
        for i in range(3):
            sconfig = {"dpid": "%016x" % (i + 1)}
            self.addSwitch("s%d" % (i + 1), **sconfig)

        # Create host nodes
        for i in range(3):
            self.addHost("h%d" % (i + 1), **host_config)

        # Add switch links
        self.addLink("s1", "s2", **link_config)
        self.addLink("s2", "s3", **link_config)

        # Add host links
        self.addLink("h1", "s1", **link_config)
        self.addLink("h2", "s2", **link_config)
        self.addLink("h3", "s3", **link_config)

topos = {"networkslicingtopo": (lambda: NetworkTopo())}

def remove_host_and_links(net, host_name):
    host = net.get(host_name)
    # Find the switch connected to the host
    for link in net.links:
        if host in (link.intf1.node, link.intf2.node):
            # Determine the switch
            if host == link.intf1.node:
                switch = link.intf2.node
            else:
                switch = link.intf1.node
            # Set link status to down
            net.configLinkStatus(host.name, switch.name, 'down')
            break  # Assuming a single link between host and switch

    # Remove the host
    net.delHost(host)

def delayed_removal(net, delay, host_name):
    time.sleep(delay)
    remove_host_and_links(net, host_name)

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

    # Create a thread to remove host h3 after 5 seconds
    removal_thread = threading.Thread(target=delayed_removal, args=(net, 5, 'h3'))
    removal_thread.start()

    # Start the CLI
    CLI(net)

    # Wait for the removal thread to finish
    removal_thread.join()

    net.stop()

