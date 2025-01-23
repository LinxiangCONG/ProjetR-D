import random
from inspect import trace

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, DEAD_DISPATCHER, CONFIG_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ipv4
from ryu.lib.packet import arp
from ryu.lib.packet import tcp
from geopy.geocoders import Nominatim
from haversine import haversine, Unit
from ryu.lib.packet import udp
from ryu.lib.packet import ether_types
import json

cities = {
    "1" : {
        "city" : "normandie",
        "server" : "es1",
        "location" : (49.0677708, 0.3138532)
    },
    "2": {
        "city" : "bordeaux",
        "server": "es2",
        "location": (44.836151, -0.580816)
    },
    "3": {
        "city" : "toulouse",
        "server": "es3",
        "location": (43.604500, 1.444000)
    },
}

servers = {
    "es1" : {
        "720p" : "192.168.50.11",
        "720p_MAC" : "00:0c:29:ec:60:c5",
        "1080p" : "192.168.60.11",
        "1080p_MAC" : "00:0c:29:ec:60:cf"
    },
    "es2": {
        "720p": "192.168.50.12",
        "720p_MAC" : "00:0c:29:38:7f:e0",
        "1080p": "192.168.60.12",
        "1080p_MAC" : "00:0c:29:38:7f:ea"
    },
    "es3": {
        "720p": "192.168.50.13",
        "720p_MAC" : "00:0c:29:1e:56:6b",
        "1080p": "192.168.60.14",
        "1080p_MAC" : "00:0c:29:1e:56:75"
    },
}

cloud_server = "192.168.20.20"

resource = {
    "co2" : {
        "720p":{
            "co2_720p_000.ts":["cloudServer"],
            "co2_720p_001.ts":["cloudServer"],
            "co2_720p_002.ts":["cloudServer"],
            "co2_720p_003.ts":["cloudServer"],
            "co2_720p_004.ts":["cloudServer"],
            "co2_720p_005.ts":["cloudServer"],
            "co2_720p_006.ts":["cloudServer"],
            "co2_720p_007.ts":["cloudServer"],
            "co2_720p_008.ts":["cloudServer"],
            "co2_720p_009.ts":["cloudServer"],
            "co2_720p_010.ts":["cloudServer"],
            "co2_720p_011.ts":["cloudServer"],
            "co2_720p_012.ts":["cloudServer"],
            "co2_720p_013.ts":["cloudServer"],
            "co2_720p_014.ts":["cloudServer"],
            "co2_720p_015.ts":["cloudServer"],
            "co2_720p_016.ts":["cloudServer"],
            "co2_720p_017.ts":["cloudServer"],
            "co2_720p_018.ts":["cloudServer"],
            "co2_720p_019.ts":["cloudServer"],
            "co2_720p_020.ts":["cloudServer"],
            "co2_720p_021.ts":["cloudServer"],
            "co2_720p_022.ts":["cloudServer"],
            "co2_720p_023.ts":["cloudServer"]
        },
        "1080p":{
            "co2_1080p_000.ts":["cloudServer"],
            "co2_1080p_001.ts":["cloudServer"],
            "co2_1080p_002.ts":["cloudServer"],
            "co2_1080p_003.ts":["cloudServer"],
            "co2_1080p_004.ts":["cloudServer"],
            "co2_1080p_005.ts":["cloudServer"],
            "co2_1080p_006.ts":["cloudServer"],
            "co2_1080p_007.ts":["cloudServer"],
            "co2_1080p_008.ts":["cloudServer"],
            "co2_1080p_009.ts":["cloudServer"],
            "co2_1080p_010.ts":["cloudServer"],
            "co2_1080p_011.ts":["cloudServer"],
            "co2_1080p_012.ts":["cloudServer"],
            "co2_1080p_013.ts":["cloudServer"],
            "co2_1080p_014.ts":["cloudServer"],
            "co2_1080p_015.ts":["cloudServer"],
            "co2_1080p_016.ts":["cloudServer"],
            "co2_1080p_017.ts":["cloudServer"],
            "co2_1080p_018.ts":["cloudServer"],
            "co2_1080p_019.ts":["cloudServer"],
            "co2_1080p_020.ts":["cloudServer"],
            "co2_1080p_021.ts":["cloudServer"],
            "co2_1080p_022.ts":["cloudServer"],
            "co2_1080p_023.ts":["cloudServer"],
        }
    },
    "train" : {
        "720p":{
        "train_720p_000.ts":["cloudServer"],
        "train_720p_001.ts":["cloudServer"],
        "train_720p_002.ts":["cloudServer"],
        "train_720p_003.ts":["cloudServer"],
        "train_720p_004.ts":["cloudServer"],
        "train_720p_005.ts":["cloudServer"],
        "train_720p_006.ts":["cloudServer"],
        "train_720p_007.ts":["cloudServer"],
        "train_720p_008.ts":["cloudServer"],
        "train_720p_009.ts":["cloudServer"],
        "train_720p_010.ts":["cloudServer"],
        "train_720p_011.ts":["cloudServer"],
        "train_720p_012.ts":["cloudServer"],
        "train_720p_013.ts":["cloudServer"],
        "train_720p_014.ts":["cloudServer"],
        "train_720p_015.ts":["cloudServer"],
        "train_720p_016.ts":["cloudServer"],
        "train_720p_017.ts":["cloudServer"],
        "train_720p_018.ts":["cloudServer"],
        "train_720p_019.ts":["cloudServer"],
        "train_720p_020.ts":["cloudServer"],
        "train_720p_021.ts":["cloudServer"]
    },
        "1080p":{
        "train_1080p_000.ts":["cloudServer"],
        "train_1080p_001.ts":["cloudServer"],
        "train_1080p_002.ts":["cloudServer"],
        "train_1080p_003.ts":["cloudServer"],
        "train_1080p_004.ts":["cloudServer"],
        "train_1080p_005.ts":["cloudServer"],
        "train_1080p_006.ts":["cloudServer"],
        "train_1080p_007.ts":["cloudServer"],
        "train_1080p_008.ts":["cloudServer"],
        "train_1080p_009.ts":["cloudServer"],
        "train_1080p_010.ts":["cloudServer"],
        "train_1080p_011.ts":["cloudServer"],
        "train_1080p_012.ts":["cloudServer"],
        "train_1080p_013.ts":["cloudServer"],
        "train_1080p_014.ts":["cloudServer"],
        "train_1080p_015.ts":["cloudServer"],
        "train_1080p_016.ts":["cloudServer"],
        "train_1080p_017.ts":["cloudServer"],
        "train_1080p_018.ts":["cloudServer"],
        "train_1080p_019.ts":["cloudServer"],
        "train_1080p_020.ts":["cloudServer"],
        "train_1080p_021.ts":["cloudServer"]
    }
    }
}

geolocator = Nominatim(user_agent="geoapi")


train = 0
co2 = 0


class L2Switch(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(L2Switch, self).__init__(*args, **kwargs)
        self.datapaths = {}

    def go(self, dp, dst_ip, src_ip, ofp_parser, msg, in_port):
        actions = []

        if dst_ip == "192.168.20.20":
            if hex(dp.id) == "0x9" or hex(dp.id) == "0x2" or hex(dp.id) == "0x1" or hex(dp.id) == "0x5" or hex(dp.id) == "0x6" or hex(dp.id) == "0x7" or hex(dp.id) == "0x8":
                actions.append(ofp_parser.OFPActionOutput(1))
            if hex(dp.id) == "0x10":
                actions.append(ofp_parser.OFPActionOutput(4))

        if dst_ip == "192.168.50.11":
            if hex(dp.id) == "0x9":
                actions.append(ofp_parser.OFPActionOutput(2))
            elif hex(dp.id) == "0x6" or hex(dp.id) == "0x7" or hex(dp.id) == "0x8" or hex(dp.id) == "0x1" or hex(dp.id) == "0x2":
                actions.append(ofp_parser.OFPActionOutput(1))
            elif hex(dp.id) == "0x5":
                actions.append(ofp_parser.OFPActionOutput(5))
            elif hex(dp.id) == "0x10":
                actions.append(ofp_parser.OFPActionOutput(2))


        if dst_ip == "192.168.50.12":
            if hex(dp.id) == "0x9":
                actions.append(ofp_parser.OFPActionOutput(2))
            elif hex(dp.id) == "0x6" or hex(dp.id) == "0x7" or hex(dp.id) == "0x8" or hex(dp.id) == "0x1" or hex(dp.id) == "0x2":
                actions.append(ofp_parser.OFPActionOutput(1))
            elif hex(dp.id) == "0x5":
                actions.append(ofp_parser.OFPActionOutput(3))
            elif hex(dp.id) == "0x10":
                actions.append(ofp_parser.OFPActionOutput(2))

        if dst_ip == "192.168.50.13":
            if hex(dp.id) == "0x9":
                actions.append(ofp_parser.OFPActionOutput(2))
            elif hex(dp.id) == "0x6" or hex(dp.id) == "0x7" or hex(dp.id) == "0x8" or hex(dp.id) == "0x1" or hex(dp.id) == "0x2":
                actions.append(ofp_parser.OFPActionOutput(1))
            elif hex(dp.id) == "0x5":
                actions.append(ofp_parser.OFPActionOutput(4))
            elif hex(dp.id) == "0x10":
                actions.append(ofp_parser.OFPActionOutput(2))

        if dst_ip == "192.168.60.11":
            if hex(dp.id) == "0x9":
                actions.append(ofp_parser.OFPActionOutput(3))
            elif hex(dp.id) == "0x8" or hex(dp.id) == "0x5" or hex(dp.id) == "0x1" or hex(dp.id) == "0x2" or hex(dp.id) == "0x6":
                actions.append(ofp_parser.OFPActionOutput(1))
            elif hex(dp.id) == "0x7":
                actions.append(ofp_parser.OFPActionOutput(5))
            elif hex(dp.id) == "0x10":
                actions.append(ofp_parser.OFPActionOutput(3))

        if dst_ip == "192.168.60.12":
            if hex(dp.id) == "0x9":
                actions.append(ofp_parser.OFPActionOutput(3))
            elif hex(dp.id) == "0x8" or hex(dp.id) == "0x5"  or hex(dp.id) == "0x1" or hex(dp.id) == "0x2" or hex(dp.id) == "0x6":
                actions.append(ofp_parser.OFPActionOutput(1))
            elif hex(dp.id) == "0x7":
                actions.append(ofp_parser.OFPActionOutput(3))
            elif hex(dp.id) == "0x10":
                actions.append(ofp_parser.OFPActionOutput(3))

        if dst_ip == "192.168.60.13":
            if hex(dp.id) == "0x9":
                actions.append(ofp_parser.OFPActionOutput(3))
            elif hex(dp.id) == "0x8" or hex(dp.id) == "0x5"  or hex(dp.id) == "0x1" or hex(dp.id) == "0x2" or hex(dp.id) == "0x6":
                actions.append(ofp_parser.OFPActionOutput(1))
            elif hex(dp.id) == "0x7":
                actions.append(ofp_parser.OFPActionOutput(4))
            elif hex(dp.id) == "0x10":
                actions.append(ofp_parser.OFPActionOutput(3))

        if dst_ip == "192.168.10.10":
            if hex(dp.id) == "0x9":
                actions.append(ofp_parser.OFPActionOutput(4))
            elif hex(dp.id) == "0x8" or hex(dp.id) == "0x5" or hex(dp.id) == "0x7" or hex(dp.id) == "0x6" or hex(dp.id) == "0x1" or hex(dp.id) == "0x2":
                actions.append(ofp_parser.OFPActionOutput(2))
            elif hex(dp.id) == "0x10":
                actions.append(ofp_parser.OFPActionOutput(1))



        # 构建 PacketOut 消息

        data = msg.data
        out = ofp_parser.OFPPacketOut(
            datapath=dp,
            buffer_id=msg.buffer_id,
            in_port=msg.match['in_port'],
            actions=actions,
            data=data,
        )
        dp.send_msg(out)

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # 定义流表规则：匹配所有流量并发送到控制器
        match = parser.OFPMatch()  # 匹配所有流量
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]  # 发送到控制器
        # 创建流表
        flow_mod = parser.OFPFlowMod(
            datapath=datapath,
            priority=0,
            match=match,
            instructions=[parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        )
        # 发送流表到交换机
        datapath.send_msg(flow_mod)


    @set_ev_cls(ofp_event.EventOFPStateChange, [MAIN_DISPATCHER, DEAD_DISPATCHER])
    def state_change_handler(self, ev):
        dp = ev.datapath

        if ev.state == MAIN_DISPATCHER:
            # 交换机已连接
            if dp.id not in self.datapaths:
                self.datapaths[dp.id] = dp
                self.logger.info("Switch %s connected", hex(dp.id))
        elif ev.state == DEAD_DISPATCHER:
            # 交换机已断开
            if dp.id in self.datapaths:
                del self.datapaths[dp.id]
                self.logger.info("Switch %s disconnected", hex(dp.id))



    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        msg = ev.msg
        dp = msg.datapath
        ofp = dp.ofproto
        ofp_parser = dp.ofproto_parser
        pkt = packet.Packet(msg.data)
        # 获取 Packet-In 的输入端口
        in_port = msg.match['in_port']

        eth = pkt.get_protocol(ethernet.ethernet)

        if not eth:
            return  # 如果不是以太网帧，直接返回

        # 检查是否为 ARP 数据包
        arp_pkt = pkt.get_protocol(arp.arp)
        # 检查是否为 IPv4 数据包
        ip_pkt = pkt.get_protocol(ipv4.ipv4)
        # 检查是否为 TCP 数据包
        tcp_pkt = pkt.get_protocol(tcp.tcp)

        actions = []
        # 若是 ARP包
        if arp_pkt:
            src_ip = arp_pkt.src_ip
            dst_ip = arp_pkt.dst_ip
            # self.logger.info("ARP Packet in switch %s - src_ip: %s, dst_ip: %s", hex(dp.id), src_ip, dst_ip)
            # 走慢的路径
            self.go(dp, dst_ip, src_ip, ofp_parser, msg, in_port)
            return

        # 若是 IPv4 包
        elif ip_pkt:
            src_ip = ip_pkt.src
            dst_ip = ip_pkt.dst
            # self.logger.info("IPv4 Packet in switch %s- src_ip: %s, dst_ip: %s", hex(dp.id), src_ip, dst_ip)
            new_dst_ip = ""
            tcp_pkt = pkt.get_protocol(tcp.tcp)
            if tcp_pkt:
                if src_ip == "192.168.10.10" and dst_ip == "192.168.20.20":
                    tcp_payload = pkt.protocols[-1]
                    if isinstance(tcp_payload, bytes):
                        http_data = tcp_payload.decode('utf-8', errors='ignore')
                        request_line = http_data.split('\r\n')[0]
                        if request_line.startswith("GET"):
                            method, uri, _ = request_line.split(' ')
                            file_name = uri.split('/')[-1]
                            self.logger.info("Captured HTTP Request - Method: %s, URI: %s, file name: %s", method, uri, file_name)

                            if "master" in file_name:
                                fileName = file_name.split('_')[0] # train, co2

                                info = self.post_request(fileName)
                                closed_server = info["closed_server"]
                                self.logger.info("closed server is : %s", closed_server)

                                missing_chunk = info["missing_chunk"]
                                self.logger.info("missing chunks are : %s", missing_chunk)
                                if len(missing_chunk) > 0 :
                                    self.send_udp_packet(dp,"00:00:00:00:00:01",servers[closed_server]["1080p_MAC"],'192.168.20.20',
                                                     servers[closed_server]['1080p'],8080,54321, missing_chunk)
                                else:
                                    self.logger.info("All resource about %s are already on %s", fileName, closed_server)
                                self.logger.info("Missing chunks %s", missing_chunk)



            # 若是 ICMP 包 或者 todo 请求包
            # if ip_pkt.proto == 1: # 是 ICMP 包吗？
                # 走慢的路径
            self.go(dp, dst_ip, src_ip, ofp_parser, msg, in_port)
            return


    # payload 是 json 数据
    def send_udp_packet(self, datapath, src_mac, dst_mac, src_ip, dst_ip, src_port, dst_port, payload):
        """
        构造并发送一个伪造的 UDP 数据包
        """
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # 构造以太网头部
        eth = ethernet.ethernet(dst=dst_mac, src=src_mac, ethertype=ether_types.ETH_TYPE_IP)

        # 构造 IPv4 头部
        ip = ipv4.ipv4(dst=dst_ip, src=src_ip, proto=17)  # proto=17 表示 UDP

        # 构造 UDP 头部
        udp_pkt = udp.udp(src_port=src_port, dst_port=dst_port)

        # 构造数据包 payload（JSON 数据）
        payload_data = json.dumps(payload).encode('utf-8')

        # 构造完整数据包
        pkt = packet.Packet()
        pkt.add_protocol(eth)
        pkt.add_protocol(ip)
        pkt.add_protocol(udp_pkt)
        pkt.add_protocol(payload_data)
        pkt.serialize()

        # 构造动作：将数据包发送到所有端口
        actions = [parser.OFPActionOutput(1)]

        # 构造 PacketOut 消息
        out = parser.OFPPacketOut(
            datapath=datapath,
            buffer_id=ofproto.OFP_NO_BUFFER,
            in_port=ofproto.OFPP_CONTROLLER,
            actions=actions,
            data=pkt.data
        )
        datapath.send_msg(out)


    def post_request(self, filename):
        import requests

        # 目标 REST 服务器的 URL
        url = "http://192.168.181.151:5000/information"

        # 要发送的请求数据（JSON 格式）
        data = {
            "filename": filename
        }

        # 可选：设置请求头
        headers = {
            "Content-Type": "application/json",  # 指定内容类型为 JSON
        }

        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            return response.json() # 如果响应是 JSON 格式
        else:
            return None