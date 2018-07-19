from scapy.all import *
from scapy.contrib.igmp import IGMP
import time
import IPy

def readIpSetFromFile(fileLocation):
      ipSet = []
      with open(fileLocation) as f:
            lines = f.readlines()
      for line in lines:
            ipSet.append(line.strip('\n'))
      return ipSet

testIpArr = readIpSetFromFile('ipSetV2.txt')


while True:
    for i in range(len(testIpArr)):
        ip = testIpArr[i]
        ipIpy = IPy.IP(ip)
        ipYan = ipIpy.strBin()[-23:]
        ipYan = '0000000100000000010111100' + ipYan
        mac = hex(int(ipYan, 2))[2:]
        if (len(hex(int(ipYan, 2))[2:]) < 12):
            for j in range(12 - len(hex(int(ipYan, 2))[2:])):
                mac = '0' + mac
        mulMac = mac[0:2] + ':' + mac[2:4] + ':' + mac[4:6] + ':' + mac[6:8] + ':' + mac[8:10] + ':' + mac[10:12]

        print ip
        print mulMac
        p_join = Ether(dst=mulMac, src='a0:8c:fd:9e:2d:f1') / IP(src='10.0.0.123', dst=ip, ttl=1) /IGMP(type=0x16,gaddr=ip,mrcode=0x00)
        sendp(p_join,iface='eth0')
        print '----------------'
    time.sleep(5)


