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
        self.accept_msg_list.append(msg)
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

        pass


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
        if msg['proposal'] > self.min_proposal:
            self.min_proposal = msg['proposal']
            rep_msg = msg.copy()
            rep_msg['type'] = 'promise'
            rep_msg['accepted_proposal'] = self.accepted_proposal
            rep_msg['accepted_proposal_val'] = self.accepted_proposal_val
            return rep_msg
        else:
            return {}

    @send
    def accept(self, msg):
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
    def prepare(self):
        self.proposal_id = self.gen_proposal_id(self.sid)
        return {'type': 'prepare', 'sid': self.sid, 'proposal': self.proposal_id}

    @send
    def propose(self, msg):
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
        rev = []
        for msg in self.promise_msg_list:
            if msg['proposal'] == self.proposal_id:
                rev.append(msg)

        if len(rev) < len(self.servers):
            return

        def compare(a, b):
            if b['accepted_proposal_val'] is None:
                return a

            if b['accepted_proposal'] > a['accepted_proposal']:
                return b

        m = reduce(compare, rev)

        self.promise_msg_list = []

        self.propose(m)


if __name__ == '__main__':
    s0 = Proposer(0, 'change')
    s1 = Acceptor(1)
    s2 = Acceptor(2)
    servers = [s0, s1, s2]
    s0.servers = servers
    s1.servers = servers
    s2.servers = servers
    s0.prepare()
    print("pause")
