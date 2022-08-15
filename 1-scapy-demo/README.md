# Scapy学习

> 因为涉及到网卡，所以该部分内容环境换到`windows`以及`pycharm`来实现

## 邮件嗅探
`mail_sniffer.py`，练习使用sniff

## ARP投毒
`arper.py`

## 笔记
### sniff
```
from scapy.all import sniff
```
>`sniff(filter="", iface="any", prn=function, count=N, store=)`
> 
> `fileter`参数允许你指定一个Berkeley数据包过滤器(Berkeley Packet Filter, BPF),用于过滤Scapy嗅探到的数据包，参数置空则代表嗅探所有数据包；如果嗅探指定如HTTP的数据包，则可以使用BPF语法，如指定BPF为`tcp port 80`
> 
> `iface`参数用于指定嗅探器要嗅探的网卡，不设置则默认所有网卡
> 
> `prn`参数用于指定一个回调函数
> 
> `count`表示嗅探包的个数，如果置空则一直嗅探
> 
> `store`为0则不会将数据保留在内存

