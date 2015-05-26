#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ast

from . import HandlerInterface
from ..node_utils import get_target_value


class AssignmentHandler(HandlerInterface):
    """
        {
            'name': '<name>'
        }
    """
    def handle(self, node):
        return get_target_value(node.target)

    def supported_types(self):
        return [ast.Assign]
