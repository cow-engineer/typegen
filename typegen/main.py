import sys
import os
import importlib
import argparse
import tempfile
import subprocess
from pprint import pformat
from typegen.generate import generate_ordered_typed_dict, save_text
from rich import print

class TypeGenCli():
    def __init__(self, args):
        self.input_dict = self.import_variable(args.file, args.var)
        self.output = args.output if args.output else None
        self.type_name = args.type_name
    
    def create_type_file(self):
        print(f"Creating type {self.type_name} {f'at path: {self.output}' if self.output else ''}")
        
        file_path, type_name = generate_ordered_typed_dict(self.input_dict, self.type_name, self.output)
        
        print(f"Creation complete\nRunning pytype test")
        
        results = self.test_new_type(self.input_dict, file_path, type_name)
        
        return results    
                     
    def import_variable(self, file_path, variable_name):
        # Extract directory and file/module name from the path
        dir_name, file_name = os.path.split(file_path)
        module_name, _ = os.path.splitext(file_name)
        
        sys.path.insert(0, dir_name or '.')
        module = importlib.import_module(module_name)
        variable_value = getattr(module, variable_name, None)

        if variable_value is None:
            print(f"Variable {variable_name} not found in {file_name}")
            quit()

        # Remove the directory from sys.path
        sys.path.pop(0)

        return variable_value
   
    def print_failure_msg(self):
        print("Oops, type creation did not pass tests. Consider reporting it: [link=https://github.com/pestosoftware/typegen/issues]Create Issue[/link]")

    def pytype_test(self,path):
        result = subprocess.run(['pytype', path])
        return result.returncode

    def test_new_type(self, input_dict, type_file_path, type_name):
        test_import_str = f'from {type_file_path.replace("/", ".").replace(".py", "")} import {type_name}\n\n'
        test_obj_str = f"test_obj: {type_name} = {pformat(input_dict, indent=4)}\n"
        test_file_str = test_import_str + test_obj_str

        # Use the tempfile module to create a temporary directory
        with tempfile.TemporaryDirectory() as tmpdirname:
            test_file_path = os.path.join(tmpdirname, f"test_{type_name}_type.py")
            save_text(test_file_path, test_file_str)
            return self.pytype_test(test_file_path)
    
def main():
    parser = argparse.ArgumentParser(description="Import a variable from a file.")
    parser.add_argument('-f', '--file', type=str, required=True, help='Path to the python file (without .py extension)')
    parser.add_argument('-v', '--var', type=str, required=True, help='Variable name in the file')
    parser.add_argument('-t', '--type-name', type=str, required=True, help='Name for the type')
    parser.add_argument('-o', '--output', type=str, default="", help='Path to the output file (default: <name of variable>.py')
    args = parser.parse_args()
    
    cli = TypeGenCli(args)
    
    result = cli.create_type_file()
    
    if result != 0:
        cli.print_failure_msg()
        
    sys.exit(result)
