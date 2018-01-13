# -*- coding: utf-8 -*-
"""
Handles ClassDef-nodes in an AST
"""
import ast

from code_visualizer.ast_parser.node_utils import get_node_name
from code_visualizer.ast_parser.parsers.interface import ParserInterface


class ClassParser(ParserInterface):
    """Return a dict of class signature
        {
            'name': '<name>',
            'bases': ['<base_name>'...]
        }
        """

    def parse(self, node):
        """Return the name/bases of base for class node.

        :param node: a supported node
        :type node: ast.ClassDef

        :return: list of dicts with name and bases for each base
        """
        return [{
            'name': node.name,
            'bases': [get_node_name(base) for base in node.bases]
        }]

    @property
    def supported_types(self):
        """
        class ClassDef(name, bases, keywords, starargs,
                       kwargs, body, decorator_list)
        """
        return ast.ClassDef,
