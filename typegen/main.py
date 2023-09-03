import sys
import os
import importlib
import argparse
import tempfile
import subprocess
from pprint import pformat
from time import sleep
from typegen.generate import generate_ordered_typed_dict, save_text

parser = argparse.ArgumentParser(description="Import a variable from a file.")
parser.add_argument('-f', '--file', type=str, required=True, help='Path to the python file (without .py extension)')
parser.add_argument('-v', '--var', type=str, required=True, help='Variable name in the file')
parser.add_argument('-t', '--type-name', type=str, required=True, help='Name for the type')
parser.add_argument('-o', '--output', type=str, default="", help='Path to the output file (default: <name of variable>.py')

args = parser.parse_args()

def import_variable(file_path, variable_name):
    # Extract directory and file/module name from the path
    dir_name, file_name = os.path.split(file_path)
    module_name, _ = os.path.splitext(file_name)

    # Add the directory to sys.path
    sys.path.insert(0, dir_name or '.')

    # Dynamically import the module
    module = importlib.import_module(module_name)

    # Get the variable's value
    variable_value = getattr(module, variable_name, None)

    if variable_value is None:
        print(f"Variable {variable_name} not found in {file_name}")
        quit()

    # Remove the directory from sys.path
    sys.path.pop(0)

    return variable_value


def pytype_test(path):
    result = subprocess.run(['pytype', path])
    return result.returncode

def run_test(input_dict, type_file_path, type_name):
    test_import_str = f'from {type_file_path.replace("/", ".").replace(".py", "")} import {type_name}\n\n'
    test_obj_str = f"test_obj: {type_name} = {pformat(input_dict, indent=4)}\n"
    test_file_str = test_import_str + test_obj_str

    # Use the tempfile module to create a temporary directory
    with tempfile.TemporaryDirectory() as tmpdirname:
        test_file_path = os.path.join(tmpdirname, f"test_{type_name}_type.py")
        save_text(test_file_path, test_file_str)
        return pytype_test(test_file_path)
    
# def pytype_test(path):
#     pass 

# def create_test(input_dict, type_file_path, type_name):
#     test_import_str = f'from {type_file_path.replace("/",".").replace(".py","")} import {type_name}\n\n'
#     test_obj_str = f"test_obj: {type_name} = {pformat(input_dict, indent=4)}\n"
#     test_file_str = test_import_str + test_obj_str
#     save_text(tests/test_{type_name}_type.py", test_file_str)
#     pytype_test(f"tests/test_{type_name}_type.py")

def main():
    input_dict = import_variable(args.file, args.var)
    output = args.output if args.output else None
    print(f"Creating type {args.type_name} {f'at path: {output}' if output else ''}")

    file_path, type_name = generate_ordered_typed_dict(input_dict, args.type_name, output)
    print(f"Creation complete")

    print(f"Running pytype test")
    results = run_test(input_dict, file_path, type_name)
    
    return results
    
if __name__ == "__main__":
    sys.exit(main())