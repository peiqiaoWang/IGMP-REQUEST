# -*- coding: utf-8 -*-
from scapy.all import *
import time

InternalNetwork = {}
# 编码器IP
InternalNetwork['EncodeIp'] = '192.168.1.150'
# 编码器MAC
InternalNetwork['EncodeMac'] = '4c:cc:6a:7b:f6:db'
# 内网分配IP
InternalNetwork['InternalHostIp'] = '192.168.1.101'
# 内网主机MAC
InternalNetwork['InternalHostMac'] = '00:0e:c6:d3:54:36'
# 内网假网关
InternalNetwork['fakeGW'] = '192.168.1.250'


OfficeNetwork = {}
# 办公网IP
OfficeNetwork['OfficeIp'] = '172.17.170.176'
# 办公网MAC
OfficeNetwork['OfficeMac'] = '00:e0:4c:36:0b:83'
# 网关MAC
OfficeNetwork['GWMac'] = "58:69:6c:5e:70:ec"
# 网关IP
OfficeNetwork['GWIp'] = "172.17.168.1"
# 外网IP
OfficeNetwork['InternetIp'] = "47.100.240.240"

interface = 'eth2'

def internalNetworkSimulator():
    eth = Ether(
        src=InternalNetwork['InternalHostMac'],
        dst=InternalNetwork['EncodeMac'],
    )
    arp = ARP(
        # 代表ARP请求或者响应
        op=2,

        # 发送方Mac地址/毒化记录中的MAC
        hwsrc=InternalNetwork['InternalHostMac'],
        # 发送方IP地址/毒化记录中的IP
        psrc=InternalNetwork['InternalHostIp'],

        # 目标Mac地址/被欺骗主机MAC
        hwdst=InternalNetwork['EncodeMac'],
        # 目标IP地址/被欺骗主机IP地址
        pdst=InternalNetwork['EncodeIp']


        # 意思就是告诉192.168.31.248这个地址的主机，IP为192.168.31.100的主机MAC地址是08:00:27:97:d1:f5
        # 如果不写目标主机的IP和MAC则默认以广播的形式发送
    )
    # scapy重载了"/"操作符，可以用来表示两个协议层的组合
    # 这里我们输出一下数据包的结构信息
    # print((eth / arp).show())
    sendp(eth/arp,iface=interface)


    eth1 = Ether(
        src=InternalNetwork['InternalHostMac'],
        dst='ff:ff:ff:ff:ff:ff'
    )

    arp1 = ARP(
        op=1,
        # 发送方Mac地址/毒化记录中的MAC
        hwsrc=InternalNetwork['InternalHostMac'],
        # 发送方IP地址/毒化记录中的IP
        psrc=InternalNetwork['InternalHostIp'],

        # 目标Mac地址/被欺骗主机MAC
        hwdst="00:00:00:00:00:00",
        # 目标IP地址/被欺骗主机IP地址
        pdst=InternalNetwork['fakeGW']
    )

    sendp(eth1 / arp1, iface=interface)


#    eth2 = Ether(
#        src=InternalNetwork['InternalHostMac'],
#        dst=InternalNetwork['EncodeMac']
#    )
#
#    ip2 = IP(
#        flags=0x02,
#        src=InternalNetwork['InternalHostIp'],
#        dst=InternalNetwork['EncodeIp']
#    )
#    icmp2 = ICMP(
#        type=8,
#
#    )
#    sendp(eth2 / ip2/ icmp2, iface=interface)

def officeNetworkSimulator():

    eth1 = Ether(
        src=OfficeNetwork['OfficeMac'],
        dst='ff:ff:ff:ff:ff:ff'
    )

    arp1 = ARP(
        op=1,
        # 发送方Mac地址/毒化记录中的MAC
        hwsrc=OfficeNetwork['OfficeMac'],
        # 发送方IP地址/毒化记录中的IP
        psrc=OfficeNetwork['OfficeIp'],

        # 目标Mac地址/被欺骗主机MAC
        hwdst="00:00:00:00:00:00",
        # 目标IP地址/被欺骗主机IP地址
        pdst=OfficeNetwork['GWIp']
    )

    sendp(eth1 / arp1, iface=interface)

#    eth2 = Ether(
#        src=OfficeNetwork['OfficeMac'],
#        dst=OfficeNetwork['GWMac']
#    )

#    ip2 = IP(
#        flags=0x02,
#
#        src=OfficeNetwork['OfficeIp'],
#        dst=OfficeNetwork['InternetIp']
#    )
#    icmp2 = ICMP(
#        type=8,
#
#    )
#    sendp(eth2 / ip2/ icmp2, iface=interface)
    # print((eth2 / ip2/ icmp2).show())

def dhcpsimulator():
    dhcp_request = Ether(src="00:e0:4c:36:0b:83",dst="ff:ff:ff:ff:ff:ff") / \
                   IP(src="0.0.0.0", dst="255.255.255.255") / \
                   scapy.all.UDP(sport=68, dport=67) / \
                   scapy.all.BOOTP(op=1,htype=0x01,xid=random.randint(0,100000),flags=0x0000,chaddr="00:e0:4c:36:0b:83".replace(":", "", 5).decode('hex')) / \
                   scapy.all.DHCP(
                       options=[("message-type", "request"),("requested_addr", "172.17.170.176"),(12,"sdn"),(55,chr(1)+chr(28)+chr(2)+chr(3)+chr(15)+chr(6)+chr(119)+chr(12)+chr(44)+chr(47)+chr(26)+chr(121)+chr(42)+chr(121)+chr(249)+chr(33)+chr(252)+chr(42)),"end"])
    # print((dhcp_request).show())
    sendp(dhcp_request, iface=interface)

flag = 0
while(1):
    officeNetworkSimulator()
    internalNetworkSimulator()
    if(flag%1800 == 0):
        dhcpsimulator()
    flag = flag + 1
    time.sleep(10)


