# parser
# -*- coding:utf-8 -*-
import re
from lexer import Lexer
'''
factor ::= Number | "(" exp ")"
term   ::= factor { ("*" | "/") factor }
exp   ::= term{ ("+" | "-") term}
'''


class Parser:
    def __init__(self):
        self.element = []

    def match(self):
        for _ in self.element:
            _.match()

    def or_(self, *args):
        self.element.append(self.Or(*args))
        return self

    def token_(self, token):
        self.element.append(self.Token(token))
        return self

    def repeat_(self, arg):
        self.element.append(self.Repeat(arg))
        return self

    class Or:
        def __init__(self, *args):
            self.element = []
            self.element.extend(args)

        def match(self):
            for _ in self.element:
                if _.match():
                    return True
            return False

    class Token:
        def __init__(self, token):
            self.token = token

        def match(self):
            try:
                if tokens[0] == self.token:
                    print(tokens.pop(0), '->', end='')
                    return True
                else:
                    return False
            except IndexError:
                return False

    class Repeat:
        def __init__(self, element):
            self.element = element

        def match(self):
            while self.element.match():
                pass


if __name__ == '__main__':
    lexer = Lexer('tokens.txt')
    tokens = lexer.get_tokens()
    print(tokens)
    parser = Parser()
    parser.or_(parser.Token('a'), parser.Token('b'))\
          .token_('c')\
          .or_(parser.Token('d'), parser.Token('e'))\
          .repeat_(parser.Token('f'))\
          .token_('g')
    parser.match()

