
# -*- coding: utf-8 -*-
# Filename : templatefile.py


def render_funciton(context, do_dots):
    c_user_name = context['user_name']
    c_product_list = context['product_list']
    c_format_price = context['format_price']

    result = []
    append_result = result.append
    extend_result = result.extend
    to_str = str
    append_result('<!DOCTYPE html>')
    extend_result(['<html><h1>Welcome,', c_user_name ,'!</h1><p>Products:</p><ul>'])

    for product in c_product_list :
        extend_result(['<li>', do_dots(product, 'name'), ':', c_format_price(do_dots(product, 'price')), '</li>'])
    return ''.join(result)


def format_price(val):
    return '${}'.format(val)


class CodeBuilder:
    INDENT_STEP = 4

    def __init__(self, indent_level= 0):
        self.code = []
        self.indent_level = indent_level

    def and_line(self, line):
        self.code.extend([' ' * self.indent_level, line, '\n'])

    def add_section(self):
        section = CodeBuilder(self.indent_level)
        self.code.append(section)
        return section

    def indent(self):
        self.indent_level += self.INDENT_STEP

    def dedent(self):
        self.indent_level -= self.INDENT_STEP

    def get_globals(self):
        assert self.indent_level == 0
        python_source = str(self)
        global_namespace = {}
        exec(python_source, global_namespace)
        return global_namespace

    def __str__(self):
        return ''.join(str(c) for c in self.code)

if __name__ == '__main__':
    builder = CodeBuilder()
    builder.and_line("def foo():")
    builder.indent()
    vars_builder = builder.add_section()
    vars_builder.and_line("print('q')")
    vars_builder.and_line("return 100")
    builder.dedent()
    g = builder.get_globals()
    print(g['foo'])

