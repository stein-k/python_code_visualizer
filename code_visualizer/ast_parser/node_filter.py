#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Filtering criteria"""
from abc import ABCMeta, abstractmethod


class Criteria(object):
    """
    Base-class for filtering criteria.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def wants_to_handle_node(self, node_parents, node):
        """Method to determine if visitor is interested in node"""
        return True

    @abstractmethod
    def wants_to_visit_descendants(self, node_parents, node):
        """Method to determine if visitor is interested in descendants"""
        return True

    @abstractmethod
    def handle_node(self, node_parents, node):
        """Method to handle node"""
        pass


class PassThroughCriteria(Criteria):
    """Criteria that visits all nodes"""
    def wants_to_handle_node(self, node_parents, node):
        return True

    def wants_to_visit_descendants(self, node_parents, node):
        return True

    def handle_node(self, node_parents, node):
        pass
