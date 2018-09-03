#-*- coding: UTF-8 -*-
from scapy.all import *
from scapy.contrib.igmpv3 import IGMPv3,IGMPv3mq,IGMP,IGMPv3gr
from scapy.contrib.igmpv3 import IGMPv3mr
import argparse


parser = argparse.ArgumentParser(description='选择网口进行引流')
parser.add_argument('--interface', help='输入对应的网口')
args = parser.parse_args()
interface = args.interface

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
        sendp(p_join, iface=interface)
        sendp(p_join, iface=interface)
        print '----------------'
    time.sleep(5)

