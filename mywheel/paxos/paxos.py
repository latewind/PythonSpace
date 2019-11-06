# -*- coding: UTF-8 -*-
import time
from functools import reduce

'''
Basic Paxos
https://zhuanlan.zhihu.com/p/31780743
'''


def send(func):
    # s0.prepare() => process(prepare)(),func = prepare; => inner(s0)
    def inner(*args):
        msg = func(*args)
        args[0].send(msg)

    return inner


class Server:
    def __init__(self, sid):
        self.sid = sid
        self.servers = []
        self.prepare_msg_list = []
        self.promise_msg_list = []
        self.accept_msg_list = []
        self.propose_msg_list = []

    def broadcast(self, msg):
        for server in self.servers:
            self.send_msg(msg, server.sid)

    def send_msg(self, msg, sid):
        print("send {} from {} to {}".format(msg, self.sid, sid))
        self.servers[sid].rev_msg(msg)

    def rev_msg(self, msg):
        if msg['type'] == 'prepare':
            self.prepare_msg_list.append(msg)

        if msg['type'] == 'promise':
            self.promise_msg_list.append(msg)

        if msg['type'] == 'accept':
            self.accept_msg_list.append(msg)

        if msg['type'] == 'propose':
            self.propose_msg_list.append(msg)

        self.set_response()

    def send(self, msg):
        if msg['type'] in ['prepare', 'propose']:
            self.broadcast(msg)
        if msg['type'] in ['promise', 'accept']:
            self.send_msg(msg, msg['sid'])


class Acceptor(Server):
    def __init__(self, sid):
        super(Acceptor, self).__init__(sid)
        self.min_proposal = 0
        self.accepted_proposal = None
        self.accepted_proposal_val = None
        self.value = None
        pass

    @send
    def promise(self, msg):
        """
        2.对prepare进行相应，如果proposal > min proposal，min proposal = proposal
        并返回已经接受的proposal value
        :param msg:
        :return:
        """
        if msg['proposal'] > self.min_proposal:
            self.min_proposal = msg['proposal']
            rep_msg = msg.copy()
            rep_msg['type'] = 'promise'
            rep_msg['accepted_proposal'] = self.accepted_proposal
            rep_msg['accepted_proposal_val'] = self.accepted_proposal_val
            return rep_msg
        else:
            # TODO 处理
            return None

    @send
    def accept(self, msg):
        """
        4. 如果 proposal 大于/等于 min_proposal,将min_proposal accepted_proposal = proposal, accepted_value = value
        返回 min_proposal
        :param msg:
        :return:
        """
        if msg['proposal'] >= self.min_proposal:
            self.min_proposal = msg['proposal']
            self.accepted_proposal = msg['proposal']
            self.accepted_proposal_val = msg['proposal_val']
            self.value = self.accepted_proposal_val

        return {'type': 'accept', 'result': self.min_proposal, 'sid': msg['sid'], 'value': self.value}

    def set_response(self):
        while self.prepare_msg_list:
            head_msg = self.prepare_msg_list.pop(0)
            if head_msg is not None:
                self.promise(head_msg)
            else:
                break
        self.process_promise_resp()

        self.process_propose_resp()

        self.process_accept_resp()

    def process_promise_resp(self):
        pass

    def process_propose_resp(self):
        while self.propose_msg_list:
            head_msg = self.propose_msg_list.pop(0)
            if head_msg is not None:
                self.accept(head_msg)
            else:
                break
        pass

    def process_accept_resp(self):
        pass


class Proposer(Acceptor):
    def __init__(self, sid, proposal_value):
        super(Proposer, self).__init__(sid)
        self.proposal_value = proposal_value
        self.proposal_id = None
        pass

    @staticmethod
    def gen_proposal_id(i):
        return int(time.time() + i)

    @send
    def prepare(self, value=None):
        """
        1.生成一个prepare请求，携带proposalID
        :param value:
        :return:
        """
        self.proposal_id = self.gen_proposal_id(self.sid)
        print(self.proposal_id)
        if value:
            self.proposal_value = value
        return {'type': 'prepare', 'sid': self.sid, 'proposal': self.proposal_id}

    @send
    def propose(self, msg):
        """
        3.2. accepted_proposal最大的value作为值，发送
        如果没有，则随意指定一个value
        :param msg:
        :return:
        """
        if msg['accepted_proposal_val'] is not None:
            proposal_value = msg['accepted_proposal_val']
        else:
            proposal_value = self.proposal_value
        return {'type': 'propose', 'proposal_val': proposal_value, 'proposal': msg['proposal'], 'sid': msg['sid']}

    def after_accept(self, msg):
        if self.proposal_id < msg['result']:
            print("retry")
            self.retry()
        else:
            print("success")

    def retry(self):
        self.prepare()

    def process_promise_resp(self):
        """
        3.1.接受promise响应，收到半数请求后，筛选出最大的accepted_proposal的value
        :return:
        """
        rev = []
        # 只接受本论发起的
        for msg in self.promise_msg_list:
            if msg['proposal'] == self.proposal_id:
                rev.append(msg)
        # 超过半数
        if len(rev) < len(self.servers) / 2:
            return

        def compare(a, b):
            if b['accepted_proposal_val'] is None:
                return a
            if a['accepted_proposal'] is None:
                return b
            if b['accepted_proposal'] >= a['accepted_proposal']:
                return b

        m = reduce(compare, rev)
        print(str(m) + "--------------")
        self.promise_msg_list = []

        self.propose(m)

    def process_accept_resp(self):
        """
        5.收到半数后，如果result大于proposal id，说明有更新的提议，重新提议
        :return:
        """
        rev = []
        # 只接受本论发起的
        for msg in self.accept_msg_list:
            if msg['proposal'] == self.proposal_id:
                rev.append(msg)
        # 超过半数
        if len(rev) < len(self.servers) / 2:
            return

        for _ in rev:
            if rev['result'] > self.proposal_id:
                self.retry()
                break


if __name__ == '__main__':
    s0 = Proposer(0, 'change')
    s1 = Acceptor(1)
    s2 = Acceptor(2)
    servers = [s0, s1, s2]
    s0.servers = servers
    s1.servers = servers
    s2.servers = servers
    s0.prepare(0)
    print("pause")
    time.sleep(1)
    s0.prepare(1)
