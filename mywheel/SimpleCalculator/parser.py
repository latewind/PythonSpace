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
            op = self.read()
            left = self.combine(left, op, self.term())
        return left

    def term(self):
        left = self.factor()
        while self.next_symbol() in ('*', '/'):
            op = self.read()
            left = self.combine(left, op, self.factor())
        return left

    def factor(self):
        next_token = self.read()
        if next_token is '(':
            expr = self.expression()
            self.read()
            return expr
        else:
            return Number(next_token)

    def next_symbol(self):
        if not len(self.tokens):
            return None
        return self.peek()

    @staticmethod
    def combine(left, op, right):
        return MathOperator(left, op, right)

    def read(self):
        return self.tokens.pop(0)

    def peek(self):
        if len(self.tokens) > 0:
            return self.tokens[0]
        else:
            return None

'''
factor ::= Number | "(" exp ")"
exp    ::= factor { ("*" | "/" | "+" | "-" ) factor }
'''


class OpPrecedenceParser(CalcParser):
    def __init__(self, file_name):
        self.precedence = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2
        }
        self.tokens = Lexer(file_name).get_tokens()
        print(self.tokens)

    def factor(self):
        next_token = self.read()
        if next_token is '(':
            expr = self.expression()
            self.read()
            return expr
        else:
            return Number(next_token)

    def express(self):
        left = self.factor()

        while self.is_op():
            op = self.read()
            right = self.do_shirt(op)
            left = self.combine(left, op, right)
        return left

    def do_shirt(self, op):
        left = self.factor()
        if self.is_op():
            n_op = self.peek()
            if self.precedence[n_op] > self.precedence[op]:
                n_op = self.read()
                right = self.do_shirt(n_op)
                return self.combine(left, n_op, right)
            else:
                return left
        return left

    def is_op(self):
        return self.peek() in ["+", "-", "*", "/"]


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

p = OpPrecedenceParser('calc.txt')
print(p.express().express())
