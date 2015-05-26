#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ast

from . import HandlerInterface


class ImportHandler(HandlerInterface):
    """
        {
            'where_to_import_from': '<where_to_import_from>',
            'what_to_import': '<what_to_import>',
            'alias': '<alias>',
            'name': '<name>'
        }
        """
    def handle(self, node):
        return [
            {
                'where_to_import_from': node.module if isinstance(node, ast.ImportFrom) else None,
                'what_to_import': name.name,
                'alias': name.asname,
                'name': name.asname if name.asname else name.name,
                'level': node.level if isinstance(node, ast.ImportFrom) else 0
            } for name in node.names]

    def supported_types(self):
        return [ast.Import, ast.ImportFrom]
