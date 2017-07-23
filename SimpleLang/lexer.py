# lexer.py
# -*- coding: utf-8 -*-
import re
import functools


class Lexer:
    def __init__(self, file_name):
        self.file_name = file_name
        self.tokens = []

    def parse_file(self):
        with open(self.file_name, 'r') as f:
            for line in enumerate(f.readlines()):
                yield from self._parse_line(line)

    def _parse_line(self, line):
        print(line[0], line[1])
        yield filter(lambda x: x is not '', re.split(r'\s', line[1]))

    def show_tokens(self):
        for i in self.tokens:
            for token in i:
                print(token)

lexer = Lexer('wind-lang.txt')
lexer_gen = lexer.parse_file()
print(next(lexer_gen))
print(next(lexer_gen))
print(next(lexer_gen))
