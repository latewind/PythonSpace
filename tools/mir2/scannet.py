from scapy.all import *
import time
from monsterdata import MonsterDropHistory, session
import datetime

KEY_HEADER = 'ddccbbaa4a000000100006f76400d4ff00000100'
SYSTEM_TEXT = 'a1becfb5cdb3a1bf'
PATTERN = r'【系统】\[(?P<monster_name>.*?)\]在\[(?P<map_name>.*?)\]被击杀，掉落了 \{\[(?P<object_name>.*?)\]'


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
    if 'Raw' not in data:
        return
    raw_hex = data['Raw'].load.hex()

    if not raw_hex.startswith('ddccbbaa'):
        return

    # 保存原包文标识
    need_save_hex = False

    # 根据消息头标识，分割消息
    msg_list = raw_hex.split('ddccbbaa')
    for msg in msg_list:
        if len(msg) > 32 and msg[32:].startswith(SYSTEM_TEXT):
            need_save_hex = True
            bs = bytes.fromhex(msg[32:])
            msg_ch = bs.decode(encoding='GB18030', errors="ignore")
            format_msg = "{}:{}".format(time.strftime('%Y-%m-%d %H:%M:%S'), msg_ch)
            print(format_msg)
            save_to_file(format_msg)

            save_to_db(format_msg, msg_ch)
    if need_save_hex:
        save_to_file(raw_hex)


def save_to_file(format_msg):
    with open("record.log", mode='a+', encoding='utf-8') as f:
        f.write(format_msg + "\n")


def save_to_db(format_msg, msg_ch):
    result = re.match(PATTERN, msg_ch)
    monster_name = ''
    map_name = ''
    object_name = ''
    if result is not None:
        monster_name = result['monster_name']
        map_name = result['map_name']
        object_name = result['object_name']
    try:
        q = MonsterDropHistory(create_date=datetime.datetime.now(),
                               monster_name=monster_name,
                               map=map_name,
                               object_name=object_name,
                               info=format_msg)
        session.add(q)
        session.commit()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    # read_pkg()
    # save_pkg()
    scan_network()
