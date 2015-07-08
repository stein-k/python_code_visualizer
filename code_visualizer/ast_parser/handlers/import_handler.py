# -*- coding: utf-8 -*-
"""
Handles Import-nodes and ImportFrom-nodes in an AST-tree
"""
import ast

from .interface import HandlerInterface


class ImportHandler(HandlerInterface):
    """
        {
            'where_to_import_from': '<where_to_import_from>',
            'what_to_import': '<what_to_import>',
            'alias': '<alias>',
            'name': '<name>',
            'level': <level>
        }
        """
    def handle(self, node):
        if isinstance(node, ast.ImportFrom):
            import_origin = node.module
            import_level = node.level
        else:
            import_origin = None
            import_level = 0
        return [
            {
                'where_to_import_from': import_origin,
                'what_to_import': name.name,
                'alias': name.asname,
                'name': name.asname if name.asname else name.name,
                'level': import_level
            } for name in node.names]

    @property
    def supported_types(self):
        return ast.Import, ast.ImportFrom
