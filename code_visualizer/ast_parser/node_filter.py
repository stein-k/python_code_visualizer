# -*- coding: utf-8 -*-
"""Filtering criteria"""


class Criteria(object):
    """
    Criteria that wants to handle and visit all nodes.
    """

    def wants_to_handle_node(self, node_parents, node):
        """Method to determine if visitor is interested in node"""
        return True

    def wants_to_visit_descendants(self, node_parents, node):
        """Method to determine if visitor is interested in descendants"""
        return True

    def handle_node(self, node_parents, node):
        """Method to handle node"""
        pass
