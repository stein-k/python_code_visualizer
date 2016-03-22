# -*- coding: utf-8 -*-
"""
Handles Assign-nodes in an AST-tree
"""
import ast

from .interface import HandlerInterface
from ..node_utils import get_node_name, get_node_value


class AssignmentHandler(HandlerInterface):
    """
        {
            'name': '<name>',
            'value': '<value>'
        }
    """
    def handle(self, node):
        """Return the name/values of target for the assignment node.

        :param node: assignment node
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
        return ast.Assign,
