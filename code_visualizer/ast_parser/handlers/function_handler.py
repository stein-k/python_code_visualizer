#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ast

from . import HandlerInterface


class FunctionHandler(HandlerInterface):
    """Returns information about the parsed function
        {
            'name': '<name>',
            'args': [{
                        'name': '<arg_name>'
                    }],
            'vararg': '<vararg_name>',
            'kwarg': '<kwargs_name>',
            'defaults': [{'value': <value>}]
        }
    """
    def handle(self, node):
        return {
            'name': node.name,
            'line_number': node.lineno,
            'col_offset': node.col_offset,
            'vararg': node.args.vararg,
            'kwarg': node.args.kwarg,
            'args': [{'name': arg.id} for arg in node.args.args],
            'defaults': [{'value': repr(default)} for default in node.args.defaults]
        }

    def supported_types(self):
        return [ast.FunctionDef]
