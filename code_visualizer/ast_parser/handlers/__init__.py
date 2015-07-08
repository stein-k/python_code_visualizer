from .assignment_handler import AssignmentHandler
from .class_handler import ClassHandler
from .function_handler import FunctionHandler
from .import_handler import ImportHandler
"""
Enables importing all handlers with "from handlers import *"
"""
__all__ = [
    AssignmentHandler,
    ClassHandler,
    FunctionHandler,
    ImportHandler
]
