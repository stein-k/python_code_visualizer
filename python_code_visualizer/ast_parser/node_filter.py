# -*- coding: utf-8 -*-
"""Filtering criteria"""


class Criteria(object):
    """
    Criteria that wants to handle and visit all nodes.
    """

    def wants_to_visit_descendants(self, node_parents, node):
        """
        Returns whether this criteria is
        interested in visiting the supplied node's children.

        :param node_parents: String containing node parents
            in order, separated by GENERATION_SEPARATOR.
        :param node: The node whose children may be visited.
        :returns: True if the nodes children are to be considered
            for handling and their children's descendants for visitation,
            False otherwise.
        """
        return True

    def handle_node(self, node_parents, node):
        """
        Method to handle node.
        Actual implementation should be provided by sub-class.
        If Criteria is not interested in node, it should pass.

        :param node_parents: String containing node parents
            in order, separated by GENERATION_SEPARATOR.
        :param node: The node whose children may be visited.
        """
        pass
