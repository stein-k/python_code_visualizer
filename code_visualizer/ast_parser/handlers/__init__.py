#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod, abstractproperty


class HandlerInterface(object):
    __metaclass__ = ABCMeta

    @abstractproperty
    def supported_types(self):
        return []

    @abstractmethod
    def handle(self, node):
        pass
