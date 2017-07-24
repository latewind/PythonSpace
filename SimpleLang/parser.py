# parser
# -*- coding:utf-8 -*-
'''
factor ::= Number | "(" exp ")"
term   ::= factor { ("*" | "/") factor }
exp   ::= term{ ("+" | "-") term}
'''


class CalcParser:
    def expression(self):
        left = self.term()
        while self.next_symbol() in ('*', '/'):
            left = self.combine()

    def term(self):
        pass

    def factor(self):
        pass

    def next_symbol(self):
        pass

    def combine(self):
        pass

