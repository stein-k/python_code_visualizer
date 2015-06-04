#!/usr/bin/env python
# -*- coding: utf-8 -*-


def get_counters_for_file(python_code_as_string):
    counters = {
        "lines": 0,
        "emptylines": 0,
        "commentline": 0
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
                counters["emptylines"] += 1

            if stripped_line.startswith("#"):
                counters["commentline"] += 1

    return counters
