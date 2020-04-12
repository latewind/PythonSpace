from scapy.all import *
import time
from monsterdata import MonsterDropHistory, session
import datetime

KEY_HEADER = 'ddccbbaa'
SYSTEM_TEXT = 'a1becfb5cdb3a1bf'
PATTERN = r'【系统】\[(?P<monster_name>.*?)\]在\[(?P<map_name>.*?)\]被击杀，掉落了 \{\[(?P<object_name>.*?)\]'
# }.
KEY_TAIL = '7d2e'
partial_list = []


def read_pkg():
    l = rdpcap("demo.pcap")
    print(l)
    print(type(l))
    for data in l:
        parse_pkg(data)


def read_pack(pkt):
    print(pkt)


# src host 43.227.222.97 7333
def scan_network():
    dpkt = sniff(prn=parse_pkg, count=0, iface='WLAN',
                 filter="dst host 192.168.1.102 port 52576")  # 这里是针对单网卡的机子，多网卡的可以在参数中指定网卡


def parse_pkg(data):
    global partial_list
    if 'Raw' not in data:
        return
    raw_hex = data['Raw'].load.hex()

    save_to_file(raw_hex, 'raw_hex.log')
    # 没有消息头，没有消息尾部，再进一步判断
    if not raw_hex.startswith(KEY_HEADER) and not raw_hex.endswith(KEY_TAIL):
        # 长度满格，且有缓存的消息头，说明是中间部分，通过，否则return
        if len(raw_hex) == 1072 and len(partial_list) > 0:
            pass
        else:
            return

    # 有消息头，没消息尾部，部分1，存起来
    if raw_hex.startswith(KEY_HEADER) and not raw_hex.endswith(KEY_TAIL):
        partial_list.append(raw_hex)
        return
    # 没消息头，没消息尾部，中间部分，存起来
    if not raw_hex.startswith(KEY_HEADER) and not raw_hex.endswith(KEY_TAIL):
        partial_list.append(raw_hex)
        return

    # 有消息尾，没消息头，partial_list里面有内容,消息尾部
    if not raw_hex.startswith(KEY_HEADER) and raw_hex.endswith(KEY_TAIL) and len(partial_list) > 0:
        partial_list.append(raw_hex)
        raw_hex = ''.join(partial_list)
        partial_list = []

    # 保存原包文标识
    need_save_hex = False

    # 根据消息头标识，分割消息
    msg_list = raw_hex.split(KEY_HEADER)
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


def save_to_file(format_msg, file_name='record.log'):
    with open(file_name, mode='a+', encoding='utf-8') as f:
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
