# token.py
# -*- coding:utf-8 -*-
import enum


class TokenType(enum.Enum):
    Keyword = enum.auto()
    Number = enum.auto()
    Identifier = enum.auto()
    String = enum.auto()
    Comment = enum.auto()


class Token:
    def __init__(self, value, token_type):
        self.value = value
        self.token_type = token_type

