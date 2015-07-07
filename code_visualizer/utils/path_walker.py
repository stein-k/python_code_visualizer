#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Utility to walk a path and filter on
some properties of the seen files and directories
"""
import os


DIRECTORY_MAX_SIZE = 32000
UNWANTED_DIRECTORIES = ['.git', '.svn']
WANTED_FILE_EXTENSIONS = ['.py']


def get_directory_structure(path):
    """
    Walks a directory-structure and returns path, file-name pairs
    if directory is not to big (nor unwanted) and file has '.py' extension
    :param path: The path to start walking from
    :return: (path, file-name) pairs
    """
    paths_to_check = [path]
    while paths_to_check:
        current_path = paths_to_check.pop(0)
        if os.path.isfile(current_path):
            return os.path.split(current_path)

        stats = os.stat(current_path)
        if stats.st_size > DIRECTORY_MAX_SIZE:
            # print("Path contains too many files: {0}".format(current_path))
            continue
        try:
            path_contents = os.listdir(current_path)
        except OSError:
            # print("Error reading path: {0}".format(current_path))
            continue
        for path_content in path_contents:
            full_path = os.path.join(current_path, path_content)
            if os.path.isfile(full_path):
                _, extension = os.path.splitext(path_content)
                if extension in WANTED_FILE_EXTENSIONS:
                    yield current_path, path_content
            elif path_content.lower() in UNWANTED_DIRECTORIES:
                continue
            elif os.path.isdir(full_path):
                paths_to_check.append(full_path)
