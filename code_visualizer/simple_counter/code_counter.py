#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .import_parser import get_import_statements


def get_counters_for_file(python_code_as_string):
    counters = {
        "lines": 0,
        "emptylines": 0,
        "commentline": 0,
        "classes": 0,
        "functions": 0,
        "imports": 0
    }

    imports = get_import_statements(python_code_as_string)
    counters["imports"] = sum([len(imps) for imps in imports.values()], 0)
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

        if not current_block_comment_string:
            if stripped_line == "":
                counters["emptylines"] += 1

            if stripped_line.startswith("class "):
                counters["classes"] += 1

            if stripped_line.startswith("def "):
                counters["functions"] += 1

            if stripped_line.startswith("#"):
                counters["commentline"] += 1

    return counters
