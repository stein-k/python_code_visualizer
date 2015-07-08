# -*- coding: utf-8 -*-
"""Utility module for syntax-tree parsing"""
import ast


GENERATION_SEPARATOR = '.'


def get_node_name(node):
    """
    Returns the name identifying the node.

    :param node: The node which to name
    :returns: The name identifying the node
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


def get_node_value(node):
    """
    Returns the value of the node.

    :param node: The node containing the value
    :return: The value of the node
    """
    if isinstance(node, ast.Attribute):
        return node.attr
    elif isinstance(node, ast.Tuple):
        return [{
            'name': get_node_name(sub_node)
            for sub_node in node.elts
            }]
    elif isinstance(node, ast.Subscript):
        return get_node_name(node.value)
    else:
        return node.id


def get_children_parent(ascendants, node):
    """
    Returns a string with current node appended
    to its parents separated by GENERATION_SEPARATOR.

    :param ascendants: The nodes ascendants separated by GENERATION_SEPARATOR
    :param node: The node to get the path to
    :returns: String of ancestors and node separated by GENERATION_SEPARATOR,
        if node is ast.Module (the base of the parse tree),
        an empty string is returned
    """
    if isinstance(node, ast.Module):
        return ''
    else:
        return GENERATION_SEPARATOR.join([ascendants, get_node_name(node)])
