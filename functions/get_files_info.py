import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'
    result = []
    for name in os.listdir(target_dir):
        try:
            name_path = target_dir + "/" + name
            size = os.path.getsize(name_path)
            is_dir = os.path.isdir(name_path)
            result.append(f"- {name}: file_size:={size} bytes, is_dir={is_dir}")
        except Exception as e:
            print(f"Error: could not read file information")
    return "\n".join(result)
    
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
        required=["directory"]
    ),  
)