#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod


class Criteria(object):
    """
    Base-class for filtering criteria.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def is_interested_in_node(self, node_parents, node):
        return True

    @abstractmethod
    def is_interested_in_children(self, node_parents, node):
        return True

    @abstractmethod
    def visit_node(self, node_parents, node):
        pass


class PassThroughCriteria(Criteria):
    def is_interested_in_node(self, node_parents, node):
        return True

    def is_interested_in_children(self, node_parents, node):
        return True

    def visit_node(self, node_parents, node):
        pass
