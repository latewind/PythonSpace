# -*- coding: utf-8


class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price


def do_dots(entity, field):
    return getattr(entity, field)
