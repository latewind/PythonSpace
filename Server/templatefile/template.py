# -*- coding: utf-8 -*-
# Filename : templatefile.py
import re
from entity.product import Product


def render_funciton(context, do_dots):
    c_user_name = context['user_name']
    c_product_list = context['product_list']
    c_format_price = context['format_price']

    result = []
    append_result = result.append
    extend_result = result.extend
    to_str = str
    append_result('<!DOCTYPE html>')
    extend_result(['<html><h1>Welcome,', c_user_name, '!</h1><p>Products:</p><ul>'])

    for product in c_product_list:
        extend_result(['<li>', do_dots(product, 'name'), ':', c_format_price(do_dots(product, 'price')), '</li>'])
    return ''.join(result)


def do_dots(obj, attr):
    return getattr(obj, attr)


def format_price(val):
    return '${}'.format(val)


class CodeBuilder:
    INDENT_STEP = 4

    def __init__(self, indent_level=0):
        self.code = []
        self.indent_level = indent_level

    def add_line(self, line):
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
        global_namespace = globals()
        exec(python_source, global_namespace)
        return global_namespace

    def __str__(self):
        return ''.join(str(c) for c in self.code)


class Template:
    def __init__(self, file):
        self.all_vars = set()
        self.loop_vars = set()
        with open(file, 'r') as f:
            self.text = f.readlines()
        print(''.join(self.text))
        self.tokens = re.split(r'(?s)({{.*?}}|{%.*?%}|{#.*?#})', ''.join(self.text))
        code = CodeBuilder()
        code.add_line('def render(context):')
        code.indent()
        vars_section = code.add_section()
        code.add_line('result = []')
        code.add_line('extend_result = result.extend')
        code.add_line('append_result = result.append')
        code.add_line('to_str = str')
        for token in self.tokens:
            if token.startswith('{#'):
                pass
            elif token.startswith("{{"):
                code.add_line("append_result({})".format(self._expr_code(token[2:-2])))
                pass
            elif token.startswith("{% for"):
                words = token[2:-2].strip().split()
                self.all_vars.add(words[3])
                self.loop_vars.add(words[1])
                code.add_line(token[3:-3] + ':')
                code.indent()
            elif token.startswith("{% end"):
                code.dedent()
            else:
                code.add_line("append_result('''{}''')".format(token))
        code.add_line("return ''.join(result)")
        code.dedent()
        for var in self.all_vars - self.loop_vars:
            vars_section.add_line("{0} = context['{0}']".format(var))
        self.render = code.get_globals()['render']

    def _expr_code(self, expr):
        funcs = []
        if '|' in expr:
            _ = expr.split('|')
            expr = _[0]
            funcs = _[1:]
        if '.' in expr:
            self.all_vars.add(expr.split('.')[0])
            expr = "do_dots({0},'{1}')".format(*expr.split('.'))
        else:
            self.all_vars.add(expr)
        for func in funcs:
            expr = '{}({})'.format(func, expr)
        return expr


if __name__ == '__main__':
    p1 = Product('car', 998)
    p2 = Product('map', 1)
    products = [p1, p2]
    user_name = 'Tom'
    context = {'product_list': products, 'user_name': user_name}
    t = Template('product.psp')
    print(t.render(context))
