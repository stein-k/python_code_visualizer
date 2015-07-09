#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Simple counter to count lines in a python file
"""


def get_counters_for_file(python_code_as_string):
    """Returns the number of empty, comment and total lines"""
    counters = {
        "lines": 0,
        "empty_lines": 0,
        "comment_lines": 0
    }

    current_block_comment_string = None

    for line in python_code_as_string.split('\n'):
        counters["lines"] += 1
        stripped_line = line.strip()

        if stripped_line.startswith("'''"):
            current_block_comment_string = "'''"
        if stripped_line.startswith('"""'):
            current_block_comment_string = '"""'

        if current_block_comment_string:
            if stripped_line.endswith(current_block_comment_string):
                current_block_comment_string = None
        else:
            if stripped_line == "":
                counters["empty_lines"] += 1

            if stripped_line.startswith("#"):
                counters["comment_lines"] += 1

    return counters
