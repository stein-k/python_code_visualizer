# -*- coding: utf-8 -*-
"""
Handles Assign-nodes in an AST
"""
import ast

from .interface import ParserInterface
from ..node_utils import get_node_name, get_node_value


class AssignmentParser(ParserInterface):
    """Return a dict of an Assignment
        {
            'name': '<name>',
            'value': '<value>'
        }
    """

    def parse(self, node):
        """Return the name/values of target for the assignment node.

        :param node: a supported node
        :type node: ast.Assign

        :return: list of dicts with name and value for each node.target
        """
        return [
            {
                'name': get_node_name(target),
                'value': get_node_value(target)
            } for target in node.targets
        ]

    @property
    def supported_types(self):
        """
        class Assign(targets, value)
        """
        return ast.Assign,
