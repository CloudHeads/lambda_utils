# -*- coding: utf-8 -*-

__author__ = """Hans Christoph Schabert"""
__email__ = 'christoph@schabert.me'
__version__ = '0.1.5'


class Event(object):
    function = None
    wrapped_function = None

    def __call__(self, function):
        self.function = function
        return self.wrapped_function
