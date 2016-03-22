# -*- coding: utf-8 -*-
"""
Interface for node-handlers
"""
from abc import ABCMeta, abstractmethod


class HandlerInterface(object):
    """Metaclass for handlers"""
    __metaclass__ = ABCMeta

    @abstractmethod
    def handle(self, node):
        """The node-handling implementation

        :param node: Node which the handler handles
        """
        pass

    @property
    @abstractmethod
    def supported_types(self):
        """List of supported types"""
        return ()
