# 引流操作介绍

## 文件目录介绍

- igmpv2-test.py

用于模拟发送igmpV2请求报文的脚本

- ipSetV2.txt

记录发送igmp请求报文，与igmpv2-test.py相关联，里面包含IP的文本

- igmpv3-test.py

用于模拟发送igmpV3请求报文的文件

- ipSetV3.txt

记录发送igmp请求报文，与igmpv3-test.py相关联，里面包含IP的文本

## 操作过程

1、把需要的码流IP写到 ipSetV2.txt 和 ipSetV3.txt （如果是PC机直连的话，建议里面只写两三个IP，不然主机估计承受不住）

2、然后采用tcpdump工具做 前后 验证 （前）

执行

```
sudo tcpdump -i eth0 host 239.1.1.1
```

然后看看有没有流量输出，没有话下一步

3、执行脚本```igmpv2-test.py```，sudo python igmpv2-test.py --interface eth1，然后再看看 步骤2 的终端，看看有没有流量输出；如果没有输出的话，在执行脚本```igmpv3-test.py```，然后再看看 步骤2 的终端，看看有没有流量输出。



大概流程就这样了
