# lexer.py
# -*- coding: utf-8 -*-
import re
import functools


class Lexer:
    def __init__(self, file_name):
        self.file_name = file_name
        self.tokens = []
        self.lexer_gen = self.parse_file()

    def parse_file(self):
        with open(self.file_name, 'r') as f:
            for line in enumerate(f.readlines()):
                yield from self._parse_line(line)

    def _parse_line(self, line):
        for token in filter(lambda x: x is not '', re.split(r'\s', line[1])):
            yield token

    def get_tokens(self):
        for token in self.lexer_gen:
            self.tokens.append(token)
        return self.tokens

lexer = Lexer('wind-lang.txt')


