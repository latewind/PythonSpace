from scapy.all import *
import time
from monsterdata import MonsterDropHistory, session
import datetime

KEY_HEADER = 'ddccbbaa4a000000100006f76400d4ff00000100'


def save_pkg():
    dpkt = sniff(count=20, iface='WLAN', filter="src host 43.227.222.97 port 7333")  # 这里是针对单网卡的机子，多网卡的可以在参数中指定网卡

    wrpcap("demo.pcap", dpkt)


def read_pkg():
    l = rdpcap("demo.pcap")
    print(l)
    print(type(l))
    for data in l:
        parse_pkg(data)


def read_pack(pkt):
    print(pkt)


def scan_network():
    dpkt = sniff(prn=parse_pkg, count=0, iface='WLAN', filter="host 43.227.222.97 7333")  # 这里是针对单网卡的机子，多网卡的可以在参数中指定网卡


def parse_pkg(data):
    if 'Raw' in data:
        # print(data['Raw'].load.hex())
        raw_hex = data['Raw'].load.hex()
        if not raw_hex.startswith('ddccbbaa'):
            return

        msg_hex = raw_hex[len(KEY_HEADER):]
        bs = bytes.fromhex(msg_hex)
        msg_ch = bs.decode(encoding='GB18030', errors="ignore")
        if msg_ch.startswith('【系统】'):
            format_msg = "{}:{}".format(time.strftime('%Y-%m-%d %H:%M:%S'), msg_ch)
            print(raw_hex)
            print(format_msg)
            with open("record.log", mode='a+', encoding='utf-8') as f:
                f.write(format_msg + "\n")
            try:
                q = MonsterDropHistory(create_date=datetime.datetime.now(), info=format_msg)
                session.add(q)
                session.commit()
            except Exception as e:
                print(e)


def save_to_file(content):
    with open("record.log", mode='a+', encoding='utf-8') as f:
        f.write(content + "\n")


if __name__ == '__main__':
    # read_pkg()
    # save_pkg()
    scan_network()
