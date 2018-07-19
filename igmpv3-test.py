from scapy.all import *
from scapy.contrib.igmpv3 import IGMPv3,IGMPv3mq,IGMP,IGMPv3gr
from scapy.contrib.igmpv3 import IGMPv3mr


def readIpSetFromFile(fileLocation):
    ipSet = []
    with open(fileLocation) as f:
        lines = f.readlines()
    for line in lines:
        ipSet.append(line.strip('\n'))
    return ipSet

testIpArr = readIpSetFromFile('ipSetV3.txt')

while True:
    for ip in testIpArr:
        p_join = Ether(dst='01:00:5e:00:00:16', src='00:0c:29:c8:31:8a') / IP(src='192.168.204.139', dst='224.0.0.22',
                                                                              tos=0xc0) / IGMPv3() / IGMPv3mr(
            numgrp=1) / IGMPv3gr(rtype=4, maddr=ip)
        print ip
        sendp(p_join, iface='eth0')
        sendp(p_join, iface='eth0')
        print '----------------'
    time.sleep(5)

