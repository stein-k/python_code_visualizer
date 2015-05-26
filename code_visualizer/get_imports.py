__author__ = 'stein'

import os
import sys
import ast


DIRECTORY_MAX_SIZE = 32000
UNWANTED_DIRECTORIES = ['inbox', 'plainfiles']

def handle_import(node):
        return [
            {
                'where_to_import_from': node.module if isinstance(node, ast.ImportFrom) else None,
                'what_to_import': name.name,
                'alias': name.asname,
                'name': name.asname if name.asname else name.name,
                'level': node.level if isinstance(node, ast.ImportFrom) else 0
            } for name in node.names]

def parse_file(python_file):
        result = []
        with open(python_file) as open_python_file:
            python_code_as_string = open_python_file.read()
            try:
                module_node = ast.parse(python_code_as_string)
            except (IndentationError, SyntaxError) as exception:
                print("Error: {} {} {}".format(python_file, exception.lineno, exception.msg))
                return result
            for node in ast.walk(module_node):
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    for import_statement in handle_import(node):
                        where_to_import_from = import_statement.get('where_to_import_from')
                        what_to_import = import_statement.get('name')
                        import_source = where_to_import_from if where_to_import_from else what_to_import
                        result.append(import_source)
        return result

def get_directory_structure(path):
    paths_to_check = [path]
    while paths_to_check:
        check_path = paths_to_check.pop(0)
        stats = os.stat(check_path)
        if stats.st_size > DIRECTORY_MAX_SIZE:
            print("Directory contains too many files: {}".format(check_path))
            continue
        try:
            path_content = os.listdir(check_path)
        except OSError:
            print("Error reading path: {}".format(check_path))
            continue
        for contained_path in path_content:
            full_path = os.path.join(check_path, contained_path)
            if contained_path.endswith('.py') and os.path.isfile(full_path):
                yield check_path, contained_path
            elif contained_path.lower() in UNWANTED_DIRECTORIES:
                continue
            elif os.path.isdir(full_path):
                paths_to_check.append(full_path)

def parse_path(path):
    if os.path.isdir(path):
        directory_structure = get_directory_structure(path)
        for directory, file_name in directory_structure.items():
            if file_name.endswith('.py'):
                file_path = os.path.join(directory, file_name)
                modules = parse_file(file_path)
                print('{file_name} : {modules}'.format(file_name=file_path, modules=modules))

if __name__ == '__main__':
    if len(sys.argv) == 2:
        parse_path(sys.argv[1])
    else:
        print("%s <directory to analyze>" % sys.argv[0])
