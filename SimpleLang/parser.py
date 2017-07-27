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
            if not _.match():
                return False
        return True

    def or_(self, *args):
        self.element.append(self.Or(*args))
        return self

    def token_(self, token):
        self.element.append(self.Token(token))
        return self

    def repeat_(self, arg):
        self.element.append(self.Repeat(arg))
        return self

    def append_(self, p):
        self.element.append(p)
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

    class Number:
        def match(self):
            try:
                if re.fullmatch('\d+', tokens[0]):
                    print(tokens.pop(0), '->', end='')
                    return True
                else:
                    return False
            except IndexError:
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
            return True


if __name__ == '__main__':
    lexer = Lexer('tokens.txt')
    tokens = lexer.get_tokens()
    print(tokens)
    expr = Parser()
    factor = Parser().or_(Parser().Number(), Parser().token_('(').append_(expr).token_(')'))
    term = Parser().append_(factor).repeat_(Parser().or_(Parser().Token('*'), Parser().Token('/')).append_(factor))
    expr = expr.append_(term).repeat_(Parser().or_(Parser().Token('+'), Parser().Token('-')).append_(term))
    expr.match()
