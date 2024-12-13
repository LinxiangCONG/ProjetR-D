from mininet.node import OVSSwitch, RemoteController, Intf, Node, Controller
from mininet.cli import CLI
from mininet.log import setLogLevel,info
from mininet.net import Mininet
from mininet.link import TCLink

setLogLevel( 'info' )

class LinuxRouter( Node ):
    "A Node with IP forwarding enabled."

    # pylint: disable=arguments-differ
    def config( self, **params ):
        super( LinuxRouter, self).config( **params )
        # Enable forwarding on the router
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( LinuxRouter, self ).terminate()


net = Mininet( switch=OVSSwitch, build=False, waitConnected=True )
net.addController( 'c0' )

info( '*** Adding switches\n' )
intfName_for_sw1_ports = ['ensXX', 'ensYY', 'ensZZ','ensAA']
sw1 = net.addSwitch("sw1", listenPort=6631, dpid="1")       # add 4 more ports
# for port in intfName_for_sw1_ports:                                 # 把网卡添加到sw1上
#     Intf(port, node=sw1)

sw2 = net.addSwitch("sw2", listenPort=6631, dpid="2")

intfName_for_sw3_ports = ['ensXX', 'ensYY', 'ensZZ','ensAA']
sw3 = net.addSwitch("sw3", listenPort=6631, dpid="3")       # add 4 more ports
# for port in intfName_for_sw3_ports:                                 # 把网卡添加到sw3上
#     Intf(port, node=sw3)

sw4 = net.addSwitch("sw4", listenPort=6631, dpid="4")

intfName_for_sw5_ports = ['ensXX', 'ensYY', 'ensZZ','ensAA']
sw5 = net.addSwitch("sw5", listenPort=6631, dpid="5")       # add 4 more ports
# for port in intfName_for_sw5_ports:                                 # 把网卡添加到sw5上
#     Intf(port, node=sw5)

sw6 = net.addSwitch("sw6", listenPort=6631, dpid="6")

intfName_for_sw7_ports = ['ensXX', 'ensYY', 'ensZZ','ensAA']
sw7 = net.addSwitch("sw7", listenPort=6631, dpid="7")       # add 4 more ports
# for port in intfName_for_sw7_ports:                                 # 把网卡添加到sw7上
#     Intf(port, node=sw7)

sw8 = net.addSwitch("sw8", listenPort=6631, dpid="8")

intfName_for_sw9_port = 'ensXX'
sw9 = net.addSwitch("sw9", listenPort=6631, dpid="9")       # add 1 more port
# Intf(intfName_for_sw9_port, node=sw9)


intfName_for_sw10_port = 'ensXX'
sw10 = net.addSwitch("sw10", listenPort=6631, dpid="10")    # add 1 more port
# Intf(intfName_for_sw10_port, node=sw10)


info( "*** Creating switches with MAC, IP and DPID\n" )
sw1.setMAC('00:00:00:00:01:01',   intf='s1-eth1')
sw1.setMAC('00:00:00:00:01:02',   intf='s1-eth2')
# sw1.setMAC('00:00:00:00:01:03',   intf='ensXX')
# sw1.setMAC('00:00:00:00:01:04',   intf='ensYY')
# sw1.setMAC('00:00:00:00:01:05',   intf='ensZZ')
# sw1.setMAC('00:00:00:00:01:06',   intf='ensAA')

sw2.setMAC('00:00:00:00:02:01', intf='s2-eth1')
sw2.setMAC('00:00:00:00:02:02', intf='s2-eth2')

sw3.setMAC('00:00:00:00:03:01', intf='s3-eth1')
sw3.setMAC('00:00:00:00:03:02', intf='s3-eth2')
# sw3.setMAC('00:00:00:00:03:03', intf='ensXX')
# sw3.setMAC('00:00:00:00:03:04', intf='ensYY')
# sw3.setMAC('00:00:00:00:03:05', intf='ensZZ')
# sw3.setMAC('00:00:00:00:03:06', intf='ensAA')

sw4.setMAC('00:00:00:00:04:01', intf='s4-eth1')
sw4.setMAC('00:00:00:00:04:02', intf='s4-eth2')

sw5.setMAC('00:00:00:00:05:01', intf='s5-eth1')
sw5.setMAC('00:00:00:00:05:02', intf='s5-eth2')
# sw5.setMAC('00:00:00:00:05:03', intf='ensXX')
# sw5.setMAC('00:00:00:00:05:04', intf='ensYY')
# sw5.setMAC('00:00:00:00:05:05', intf='ensZZ')
# sw5.setMAC('00:00:00:00:05:06', intf='ensAA')

sw6.setMAC('00:00:00:00:06:01', intf='s6-eth1')
sw6.setMAC('00:00:00:00:06:02', intf='s6-eth2')

sw7.setMAC('00:00:00:00:07:01', intf='s7-eth1')
sw7.setMAC('00:00:00:00:07:02', intf='s7-eth2')
# sw7.setMAC('00:00:00:00:07:03', intf='ensXX')
# sw7.setMAC('00:00:00:00:07:04', intf='ensYY')
# sw7.setMAC('00:00:00:00:07:05', intf='ensZZ')
# sw7.setMAC('00:00:00:00:07:06', intf='ensAA')

sw8.setMAC('00:00:00:00:08:01', intf='s8-eth1')
sw8.setMAC('00:00:00:00:08:02', intf='s8-eth2')

sw9.setMAC('00:00:00:00:09:01', intf='s9-eth1')
sw9.setMAC('00:00:00:00:09:02', intf='s9-eth2')
# sw9.setMAC('00:00:00:00:09:03', intf='ensXX')
# sw9.setMAC('00:00:00:00:09:04', intf='ensYY')
# sw9.setMAC('00:00:00:00:09:05', intf='ensZZ')
sw9.setIP("100.100.100.254", prefixLen=24, intf="s9-eth1")
sw9.setIP("300.300.300.254", prefixLen=24, intf="s9-eth2")
sw9.setIP("500.500.500.254", prefixLen=24, intf="s9-eth3")
sw9.setIP("700.700.700.254", prefixLen=24, intf="s9-eth4")
sw9.setIP("66.66.66.254",    prefixLen=24, intf="s9-eth5")

sw10.setMAC('00:00:00:00:10:01', intf='s10-eth1')
sw10.setMAC('00:00:00:00:10:02', intf='s10-eth2')
# sw10.setMAC('00:00:00:00:10:03', intf='ensXX')
# sw10.setMAC('00:00:00:00:10:04', intf='ensYY')
# sw10.setMAC('00:00:00:00:10:05', intf='ensZZ')
sw10.setIP("100.100.100.253", prefixLen=24, intf="s10-eth1")
sw10.setIP("300.300.300.253", prefixLen=24, intf="s10-eth2")
sw10.setIP("500.500.500.253", prefixLen=24, intf="s10-eth3")
sw10.setIP("700.700.700.253", prefixLen=24, intf="s10-eth4")
sw10.setIP("9.9.9.253", prefixLen=24, intf="s10-eth5")


info("*** adding hosts ***\n")
c1 = net.addHost("c1", mac="20:00:00:00:00:01", ip="66.66.66.66/24")
cs = net.addHost("cs",mac="10:00:00:00:00:01", ip="9.9.9.9/24")


info("*** adding links with constraint\n")
net.addLink(cs,sw10, intfName1="cs1-eth1", intfName2="sw10-eth5")

net.addLink(sw10,sw1,intfName1='sw10-eth1', intfName2='s1-eth1')
net.addLink(sw10,sw3,intfName1='sw10-eth2', intfName2='s3-eth1')
net.addLink(sw10,sw5,intfName1='sw10-eth3', intfName2='s5-eth1')
net.addLink(sw10,sw7,intfName1='sw10-eth4', intfName2='s7-eth1')

net.addLink(sw1,sw2, intfName1='sw1-eth2', intfName2='sw2-eth1', bw=10, delay='5ms', loss=2)
net.addLink(sw3,sw4, intfName1='sw3-eth2', intfName2='sw4-eth1', bw=10, delay='5ms', loss=2)
net.addLink(sw5,sw6, intfName1='sw5-eth2', intfName2='sw6-eth1', bw=10, delay='5ms', loss=2)
net.addLink(sw7,sw8, intfName1='sw7-eth2', intfName2='sw8-eth1', bw=10, delay='5ms', loss=2)

net.addLink(sw2,sw9,  intfName1='sw2-eth2', intfName2='sw9-eth1', bw=10, delay='5ms', loss=2)
net.addLink(sw4,sw9,  intfName1='sw4-eth2', intfName2='sw9-eth2', bw=10, delay='5ms', loss=2)
net.addLink(sw6,sw9,  intfName1='sw6-eth2', intfName2='sw9-eth3', bw=10, delay='5ms', loss=2)
net.addLink(sw8,sw9,  intfName1='sw8-eth2', intfName2='sw9-eth4', bw=10, delay='5ms', loss=2)

net.addLink(sw9,c1, intfName1='sw9-eth5', intfName2='c1-eth1')



net.build()















