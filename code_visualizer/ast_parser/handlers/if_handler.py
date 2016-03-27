# -*- coding: utf-8 -*-
"""
Handles If-nodes in an AST
"""
import ast

from ast_parser.handlers.interface import HandlerInterface


class IfHandler(HandlerInterface):
    """Returns dict of if statement
        {
            'test': '<test>',
            'body': '<body>',
            'orelse': '<orelse>'
        }
    """
    def handle(self, node):
        """Return dict about supported node

        :param node: a supported node
        :type node: ast.If

        :return: dictionary from node statement
        """
        return {
            'test': node.test,
            'body': node.body,
            'orelse': node.orelse,
        }

    @property
    def supported_types(self):
        """
        class If(test, body, orelse)
        """
        return ast.If,
