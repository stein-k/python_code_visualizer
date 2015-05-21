#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

class Criteria(object):
    """
    Base-class for filtering criteria.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def return_node(self, node_parents_types, node):
        return True

    @abstractmethod
    def visit_children(self, node_parents_types, node):
        return True

class PassThroughCriteria(Criteria):
    def return_node(self, node_parents_types, node):
        return True

    def visit_children(self, node_parents_types, node):
        return True
