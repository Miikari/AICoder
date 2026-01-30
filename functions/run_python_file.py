import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

    valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

    not_valid = validity_check(file_path, valid_target_file, target_file)
    if not_valid:
        return not_valid
    try:
        command = ["python", target_file]
        if args:
            command.extend(args)

        process = subprocess.run(
            command, 
            cwd=working_directory, 
            capture_output=True, 
            text=True, 
            timeout=30
            )
    except Exception as e:
        return f'Error: could not run the target file: {target_file}'
    
    returning_string = ""
    if process.returncode != 0:
        returning_string += "Process exited with code X"
    if not process.stdout or process.stderr:
        returning_string += "No output produced"
    else:
        returning_string += f"STDERR: {process.stderr} + STDOUT: {process.stdout}"

    return returning_string

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="runs the python file if found and accessible",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="file path to find the file to run",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="additional arguments possibly",
                items=types.Schema(
                    type=types.Type.STRING,
                ),
            )
        },
        required=["file_path"]
    ),
)

def validity_check(file_path, valid_target_file, target_file):
    if not valid_target_file:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    if not file_path.endswith('py'):
        return f'Error: "{file_path}" is not a Python file'
    return None