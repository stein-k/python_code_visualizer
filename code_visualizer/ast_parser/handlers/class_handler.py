#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ast

from .interface import HandlerInterface
from ..node_utils import get_node_name


class ClassHandler(HandlerInterface):
    """
        {
            'name': '<name>',
            'bases': ['<base_name>'...]
        }
        """
    def handle(self, node):
        bases = []
        for base in node.bases:
            bases.append(get_node_name(base))
        return [{
            'name': node.name,
            'bases': bases
        }]

    def supported_types(self):
        return [ast.ClassDef]
