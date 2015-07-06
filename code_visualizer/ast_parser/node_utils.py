#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ast


GENERATION_SEPARATOR = '.'


def get_node_name(node):
    """
    Returns the name identifying the node

    :param node The node which to name
    :return: The name identifying the node
    """
    if isinstance(node, ast.Attribute):
        return node.attr
    elif isinstance(node, ast.Name):
        return node.id
    elif isinstance(node, ast.Call):
        return get_node_name(node.func)

    elif hasattr(node, 'name') and node.name:
        return node.name
    else:
        format_dict = {
            'type': type(node).__name__,
            'line': None,
            'col': None
        }
        if hasattr(node, 'lineno'):
            format_dict['line'] = node.lineno
        if hasattr(node, 'col_offset'):
            format_dict['col'] = node.col_offset
        return "{type}[{line}:{col}]".format(**format_dict)


def get_target_value(target):
    """
    Returns the value of the node

    :param target: The node containing the value
    :return: The value of the node
    """
    if isinstance(target, ast.Attribute):
        return target.attr
    elif isinstance(target, ast.Tuple):
        return [{
            'name': get_node_name(sub_target)
            for sub_target in target.elts
            }]
    elif isinstance(target, ast.Subscript):
        return get_node_name(target.value)
    else:
        return target.id


def get_children_parent(node, node_parent):
    """
    Returns a string with current node appended
    to its parents separated by GENERATION_SEPARATOR
    :param node: The node to get the path to
    :param node_parent: The nodes parents separated by GENERATION_SEPARATOR
    :return: String with path through generations for node
    """
    return '' \
        if isinstance(node, ast.Module) \
        else GENERATION_SEPARATOR.join([node_parent, get_node_name(node)])
