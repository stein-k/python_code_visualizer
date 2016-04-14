# -*- coding: utf-8 -*-
"""
Handles FunctionDef-nodes in an AST
"""
import ast

from .interface import ParserInterface
from ..node_utils import get_node_name


class FunctionParser(ParserInterface):
    """Returns a dict of the parsed function
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

    def parse(self, node):
        """Return information about function node.

        :param node: a function definition node
        :type node: ast.FunctionDef

        :return: list of dictionaries of function name/arguments
        """
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

    @property
    def supported_types(self):
        """
        class FunctionDef(name, args, body, decorator_list, returns)
        """
        return ast.FunctionDef,
