# -*- coding: utf-8 -*-
"""
Handles FunctionDef-nodes in an AST-tree
"""
import ast

from .interface import HandlerInterface
from ..node_utils import get_node_name


class FunctionHandler(HandlerInterface):
    """Returns information about the parsed function
        {
            'name': '<name>',
            'vararg': '<vararg_name>',
            'kwarg': '<kwargs_name>',
            'args': [{
                        'name': '<arg_name>'
                    }],
            'defaults': [{'value': <value>}]
        }
    """
    def handle(self, node):
        return [{
            'name': node.name,
            'vararg': node.args.vararg,
            'kwarg': node.args.kwarg,
            'args': [{'name': get_node_name(arg)} for arg in node.args.args],
            'defaults': [
                {'value': repr(default)}
                for default in node.args.defaults
                ]
        }]

    def supported_types(self):
        return ast.FunctionDef,
