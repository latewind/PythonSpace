
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





