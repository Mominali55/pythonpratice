#!/usr/bin/env python3
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel

class DDoSTopo(Topo):
    "Simple DDoS topology example: 1 switch, 3 hosts."

    def build(self):
        # Add switch
        s1 = self.addSwitch('s1')

        # Add hosts
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')

        # Create links with 10Mbps bandwidth limit to allow easy saturation
        linkopts = {'bw': 10}
        
        self.addLink(s1, h1, **linkopts)
        self.addLink(s1, h2, **linkopts)
        self.addLink(s1, h3, **linkopts)

def run_topo():
    topo = DDoSTopo()
    net = Mininet(topo=topo, link=TCLink)
    net.start()
    
    print("DDoS Topology Started.")
    print("Default Links: 10Mbps bandwidth.")
    print("Network ready. Starting CLI...")
    
    CLI(net)
    
    print("Stopping network...")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run_topo()
