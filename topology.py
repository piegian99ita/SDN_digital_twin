#!/usr/bin/python3

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
        

        for i in range(3):
            sconfig = {"dpid": "%016x" % (i + 1)}
            self.addSwitch("s%d" % (i + 1), **sconfig)

        # Create host nodes
        for i in range(3):
            self.addHost("h%d" % (i + 1), **host_config)

        
        # Add switch links
        self.addLink("s1", "s2", **link_config)
        self.addLink("s2", "s3", **link_config)
        #self.addLink("s2", "s3", **link_config)

        # Add host links
        self.addLink("h1", "s1", **link_config)
        self.addLink("h2", "s2", **link_config)
        self.addLink("h3", "s3", **link_config)
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
    CLI(net)
    net.stop()