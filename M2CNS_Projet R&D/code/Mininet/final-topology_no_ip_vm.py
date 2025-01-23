import subprocess
from distutils.command.build import build

from mininet.node import OVSSwitch, RemoteController, Intf, Node, Controller
from mininet.cli import CLI
from mininet.log import setLogLevel,info
from mininet.net import Mininet
from mininet.link import TCLink

setLogLevel( 'info' )

def add_port_to_switch(switch, interface):
    """
    使用 ovs-vsctl 命令将物理接口添加到指定的交换机。
    :param switch: 交换机名称，例如 'sw9'
    :param interface: 物理接口名称，例如 'ens37'
    """
    try:
        subprocess.run(["sudo", "ovs-vsctl", "add-port", switch, interface], check=True)
        print(f"Successfully added {interface} to {switch}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to add {interface} to {switch}: {e}")


def list_ports(switch):
    """
    列出指定交换机的端口。
    :param switch: 交换机名称，例如 'sw9'
    """
    try:
        result = subprocess.run(["sudo", "ovs-vsctl", "list-ports", switch],
                                capture_output=True, text=True, check=True)
        print(f"Ports on {switch}:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to list ports on {switch}: {e}")


net = Mininet( switch=OVSSwitch, controller=RemoteController, build=False, waitConnected=True , link=TCLink)
ryu = RemoteController('ryu', controller=RemoteController, ip='192.168.181.144', port=6633, protocols="OpenFlow13")
net.addController(ryu)

info( '*** Adding switches\n' )
sw1 = net.addSwitch("sw1", listenPort=6631,cls=OVSSwitch, dpid="01", protocols='OpenFlow13')
sw2 = net.addSwitch("sw2", listenPort=6631,cls=OVSSwitch, dpid="02", protocols='OpenFlow13')
# sw3 = net.addSwitch("sw3", listenPort=6631, dpid="03")
# sw4 = net.addSwitch("sw4", listenPort=6631, dpid="04")
sw5 = net.addSwitch("sw5", listenPort=6631,cls=OVSSwitch, dpid="05", protocols='OpenFlow13')
sw6 = net.addSwitch("sw6", listenPort=6631,cls=OVSSwitch, dpid="06", protocols='OpenFlow13')
sw7 = net.addSwitch("sw7", listenPort=6631,cls=OVSSwitch, dpid="07", protocols='OpenFlow13')
sw8 = net.addSwitch("sw8", listenPort=6631,cls=OVSSwitch, dpid="08", protocols='OpenFlow13')
sw9 = net.addSwitch("sw9", listenPort=6631,cls=OVSSwitch, dpid="09", protocols='OpenFlow13')
sw10 = net.addSwitch("sw10", listenPort=6631,cls=OVSSwitch, dpid="10", protocols='OpenFlow13')


# info("*** adding hosts ***\n")
# c1 = net.addHost("c1", mac="20:00:00:00:00:01", ip="192.168.10.10/24")
# cs = net.addHost("cs",mac="10:00:00:00:00:01", ip="192.168.10.20/24")


info("*** adding links with constraint\n")
# net.addLink(cs,sw10, intfName1="cs-eth1", intfName2="sw10-eth5")

net.addLink(sw10,sw1,intfName1='sw10-eth1', intfName2='sw1-eth1', bw=10, delay='300ms')  # Request / Reply
# net.addLink(sw10,sw3,intfName1='sw10-eth2', intfName2='sw3-eth1', bw=100, delay='100ms') # 480p
net.addLink(sw10,sw5,intfName1='sw10-eth3', intfName2='sw5-eth1', bw=500, delay='100ms') # 720p
net.addLink(sw10,sw7,intfName1='sw10-eth4', intfName2='sw7-eth1', bw=1000, delay='10ms') # 1080p

net.addLink(sw1,sw2, intfName1='sw1-eth2', intfName2='sw2-eth1', bw=10, delay='300ms') # Request / Reply
# net.addLink(sw3,sw4, intfName1='sw3-eth2', intfName2='sw4-eth1', bw=100, delay='100ms') # 480p
net.addLink(sw5,sw6, intfName1='sw5-eth2', intfName2='sw6-eth1', bw=500, delay='200ms')  # 720p
net.addLink(sw7,sw8, intfName1='sw7-eth2', intfName2='sw8-eth1', bw=1000, delay='10ms') # 1080p

net.addLink(sw2,sw9,  intfName1='sw2-eth2', intfName2='sw9-eth1', bw=10, delay='300ms') # Request / Reply
# net.addLink(sw4,sw9,  intfName1='sw4-eth2', intfName2='sw9-eth2', bw=10, delay='100ms') # 480p
net.addLink(sw6,sw9,  intfName1='sw6-eth2', intfName2='sw9-eth3', bw=500, delay='100ms') # 720p
net.addLink(sw8,sw9,  intfName1='sw8-eth2', intfName2='sw9-eth4', bw=1000, delay='10ms') # 1080p

# net.addLink(sw9,c1, intfName1='sw9-eth5', intfName2='c1-eth1')


info( "*** Creating switches with MAC, IP and DPID\n" )
sw1.setMAC('00:00:00:00:01:01', intf='sw1-eth1')
sw1.setMAC('00:00:00:00:01:02', intf='sw1-eth2')

sw2.setMAC('00:00:00:00:02:01', intf='sw2-eth1')
sw2.setMAC('00:00:00:00:02:02', intf='sw2-eth2')

# sw3.setMAC('00:00:00:00:03:01', intf='sw3-eth1')
# sw3.setMAC('00:00:00:00:03:02', intf='sw3-eth2')
#
# sw4.setMAC('00:00:00:00:04:01', intf='sw4-eth1')
# sw4.setMAC('00:00:00:00:04:02', intf='sw4-eth2')

sw5.setMAC('00:00:00:00:05:01', intf='sw5-eth1')
sw5.setMAC('00:00:00:00:05:02', intf='sw5-eth2')

sw6.setMAC('00:00:00:00:06:01', intf='sw6-eth1')
sw6.setMAC('00:00:00:00:06:02', intf='sw6-eth2')

sw7.setMAC('00:00:00:00:07:01', intf='sw7-eth1')
sw7.setMAC('00:00:00:00:07:02', intf='sw7-eth2')

sw8.setMAC('00:00:00:00:08:01', intf='sw8-eth1')
sw8.setMAC('00:00:00:00:08:02', intf='sw8-eth2')

sw9.setMAC('00:00:00:00:09:01', intf='sw9-eth1')
# sw9.setMAC('00:00:00:00:09:02', intf='sw9-eth2')
sw9.setMAC('00:00:00:00:09:03', intf='sw9-eth3')
sw9.setMAC('00:00:00:00:09:04', intf='sw9-eth4')
# sw9.setMAC('00:00:00:00:09:05', intf='sw9-eth5')

sw10.setMAC('00:00:00:00:10:01', intf='sw10-eth1')
# sw10.setMAC('00:00:00:00:10:02', intf='sw10-eth2')
sw10.setMAC('00:00:00:00:10:03', intf='sw10-eth3')
sw10.setMAC('00:00:00:00:10:04', intf='sw10-eth4')
# sw10.setMAC('00:00:00:00:10:05', intf='sw10-eth5')

net.build()
net.start()

info("*** Adding physical interfaces\n")
# host
add_port_to_switch("sw9", "ens37")
# cloud server
add_port_to_switch("sw10", "ens36")
# 720p
add_port_to_switch("sw5","ens38")
add_port_to_switch("sw5","ens41")
add_port_to_switch("sw5","ens42")
# 1080p
add_port_to_switch("sw7","ens39")
add_port_to_switch("sw7","ens40")
add_port_to_switch("sw7","ens43")

info("*** Listing ports on switches\n")
list_ports("sw9")
list_ports("sw10")
list_ports("sw5")
list_ports("sw7")

CLI(net)
net.stop()















