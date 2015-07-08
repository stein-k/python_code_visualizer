# -*- coding: utf-8 -*-
"""Filtering criteria"""


class Criteria(object):
    """
    Criteria that wants to handle and visit all nodes.
    """

    def wants_to_handle_node(self, node_parents, node):
        """
        Returns whether this criteria is
        interested in handling the supplied node.

        :param node_parents: String containing node parents
            in order, separated by GENERATION_SEPARATOR.
        :param node: The node which may be handled.
        :returns: True if the handle_node() method should
            be called on the node, False otherwise.
        """
        return True

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

        :param node_parents: String containing node parents
            in order, separated by GENERATION_SEPARATOR.
        :param node: The node whose children may be visited.
        """
        pass
