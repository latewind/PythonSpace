from scapy.all import *
import time
from monsterdata import MonsterDropHistory, session
import datetime

KEY_HEADER = 'ddccbbaa'
SYSTEM_TEXT = 'a1becfb5cdb3a1bf'
PATTERN = r'【系统】\[(?P<monster_name>.*?)\]在\[(?P<map_name>.*?)\]被击杀，掉落了 \{\[(?P<object_name>.*?)\]'
# }.
KEY_TAIL = '7d2e'
LEFT_BRACE = '5b'
partial_list = []
partial = False


def read_pkg():
    l = rdpcap("demo.pcap")
    print(l)
    print(type(l))
    for data in l:
        parse_pkg(data)


#
# dst host 192.168.1.102 port 52576
def scan_network():
    dpkt = sniff(prn=parse_pkg, count=0, iface='WLAN',
                 filter="dst host 192.168.1.102 port 52576")  # 这里是针对单网卡的机子，多网卡的可以在参数中指定网卡


def parse_pkg(data):
    global partial_list
    global partial
    if 'Raw' not in data:
        return
    raw_hex = data['Raw'].load.hex()
    save_to_file(raw_hex, 'raw_hex_new.log')

    # 分段头部
    if len(raw_hex) == 1072 and raw_hex.startswith(KEY_HEADER):
        partial = True
        partial_list.append(raw_hex)
        return
    # 分段中间部位
    if len(raw_hex) == 1072 and partial is True:
        partial_list.append(raw_hex)
        return
    # 分段结尾
    if len(raw_hex) < 1072 and partial is True:
        # 结束分段
        partial_list.append(raw_hex)
        raw_hex = ''.join(partial_list)
        partial_list.clear()
        partial = False

    # 不是标准消息，返回
    if not raw_hex.startswith(KEY_HEADER):
        return
    # 保存原包文标识
    need_save_hex = False
    # 按照 【系统】 分割
    msg_list = raw_hex.split(SYSTEM_TEXT)
    for msg in msg_list:
        if len(msg) > 0 and msg.startswith(LEFT_BRACE):
            need_save_hex = True
            bs = bytes.fromhex(SYSTEM_TEXT + msg)
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
