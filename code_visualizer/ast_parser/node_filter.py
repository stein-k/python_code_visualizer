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
    def is_interested_in_node(self, node_parents, node):
        """Method to determine if visitor is interested in node"""
        return True

    @abstractmethod
    def is_interested_in_children(self, node_parents, node):
        """Method to determine if visitor is interested in nodes children"""
        return True

    @abstractmethod
    def visit_node(self, node_parents, node):
        """Method to handle node"""
        pass


class PassThroughCriteria(Criteria):
    """Criteria that visits all nodes"""
    def is_interested_in_node(self, node_parents, node):
        return True

    def is_interested_in_children(self, node_parents, node):
        return True

    def visit_node(self, node_parents, node):
        pass
