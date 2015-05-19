#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod


"""
Takes a dictionary of nodes with the following structure:
    {
        'name' : {
            'type': '<type>',
            'line_number': XXX,
            'col_number' : YYY,
            'structure' : {},
            'children' : {

            }
        }
    }
where the 'children' key contain 0 or more node-dictionaries.

Returns the fields queried for from the nodes matching the filter.
"""

class NodeFilter(object):

    def __init__(self, node_tree):
        self.node_tree = node_tree

    def filter(self, criteria):
        assert(isinstance(criteria, Criteria))


class Criteria(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def match(self):
        return False

