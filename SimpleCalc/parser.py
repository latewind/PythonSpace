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
            print('express')
            self.tokens.pop(0)
            left = self.combine(left, self.term())
        return left

    def term(self):
        left = self.factor()
        while self.next_symbol() in ('*', '/'):
            left = self.combine(left, self.factor())
        return left

    def factor(self):
        return Number(self.tokens.pop(0))

    def next_symbol(self):
        if not len(self.tokens):
            return None
        return self.tokens[0]

    def combine(self, left, right):

        return PlusOperator(left, right)


class Expression:
    def __init__(self, left, right):
        self.left = left
        self.right = right


class PlusOperator(Expression):
    def express(self):
        return self.left.express() + self.right.express()


class MinusOperator(Expression):
    def express(self):
        return self.left.express() - self.right.express()


class MultiOperator(Expression):
    def express(self):
        return self.left.express() * self.right.express()


class DivOperator(Expression):
    def express(self):
        return self.left.express() / self.right.express()


class Number(Exception):
    def __init__(self, val):
        self.val = val

    def express(self):
        return int(self.val)

c = CalcParser('calc.txt')
#print(type(c.expression()))
print(c.expression().express())