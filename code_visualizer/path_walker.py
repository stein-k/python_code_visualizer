#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


DIRECTORY_MAX_SIZE = 32000
UNWANTED_DIRECTORIES = ['.git', '.svn']
WANTED_FILE_EXTENSIONS = ['.py']


def get_directory_structure(path):
    """
    Walks a directory-structure and returns path, file-name pairs
    if directory is not to big (nor unwanted) and file has '.py' extension
    :param path: The path to start walking from
    :return: path, file-name pairs
    """
    paths_to_check = [path]
    while paths_to_check:
        check_path = paths_to_check.pop(0)
        stats = os.stat(check_path)
        if stats.st_size > DIRECTORY_MAX_SIZE:
            # print("Directory contains too many files: {0}".format(check_path))
            continue
        try:
            path_content = os.listdir(check_path)
        except OSError:
            # print("Error reading path: {0}".format(check_path))
            continue
        for sub_path in path_content:
            full_path = os.path.join(check_path, sub_path)
            if os.path.isfile(full_path):
                file_name, extension = os.path.splitext(sub_path)
                if extension in WANTED_FILE_EXTENSIONS:
                    yield check_path, sub_path
            elif sub_path.lower() in UNWANTED_DIRECTORIES:
                continue
            elif os.path.isdir(full_path):
                paths_to_check.append(full_path)
