# -*- coding: utf-8 -*-
"""
Interface for node-parsers
"""
from abc import ABCMeta, abstractmethod


class ParserInterface(object):
    """Metaclass for parsers"""
    __metaclass__ = ABCMeta

    @abstractmethod
    def parse(self, node):
        """The node-handling implementation

        :param node: Node which the handler handles
        """
        pass

    @property
    @abstractmethod
    def supported_types(self):
        """List of supported types"""
        return ()
