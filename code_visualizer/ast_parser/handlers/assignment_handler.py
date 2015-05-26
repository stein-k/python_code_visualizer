#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ast

from .interface import HandlerInterface
from ..node_utils import get_target_value


class AssignmentHandler(HandlerInterface):
    """
        {
            'name': '<name>'
        }
    """
    def handle(self, node):
        target_value = get_target_value(node.target)
        return target_value if isinstance(target_value, list) else [target_value]

    def supported_types(self):
        return [ast.Assign]
