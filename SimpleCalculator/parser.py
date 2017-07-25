# parser
# -*- coding:utf-8 -*-
from lexer import Lexer

'''
factor ::= Number | "(" exp ")"
term   ::= factor { ("*" | "/") factor }
exp   ::= term{ ("+" | "-") term}
'''


class CalcParser:
    def __init__(self, file_name):
        self.tokens = Lexer(file_name).get_tokens()
        print(self.tokens)

    def expression(self):
        left = self.term()
        while self.next_symbol() in ('+', '-'):
            op = self.tokens.pop(0)
            left = self.combine(left, op, self.term())
        return left

    def term(self):
        left = self.factor()
        while self.next_symbol() in ('*', '/'):
            op = self.tokens.pop(0)
            left = self.combine(left, op, self.factor())
        return left

    def factor(self):
        return Number(self.tokens.pop(0))

    def next_symbol(self):
        if not len(self.tokens):
            return None
        return self.tokens[0]
    @staticmethod
    def combine(left, op, right):

        return MathOperator(left, op, right)


class Expression:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class MathOperator(Expression):
    def express(self):
        return eval('self.left.express() {} self.right.express()'.format(self.op))


class Number(Exception):
    def __init__(self, val):
        self.val = val

    def express(self):
        return int(self.val)

c = CalcParser('calc.txt')
print(c.expression().express())
