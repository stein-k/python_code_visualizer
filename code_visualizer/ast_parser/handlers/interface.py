#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Interface for node-handlers
"""
from abc import ABCMeta, abstractmethod


class HandlerInterface(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def supported_types(self):
        """List of supported types"""
        return []

    @abstractmethod
    def handle(self, node):
        """The node-handling implementation"""
        pass
