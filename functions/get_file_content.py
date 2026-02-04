from pathlib import Path
import os
from google.genai import types

MAX_CHARS = 10000

def safe_path(working_directory: str, file_path: str) -> Path:
    root = Path(working_directory).resolve()
    candidate = root / file_path
    if candidate.exists() and candidate.is_symlink():
        raise ValueError("Symlink access forbidden")
    
    target = candidate.resolve(strict=False)

    if not target.is_relative_to(root):
        raise ValueError("Access outside working directory is forbidden")
    return target

def get_file_content(working_directory, file_path):
    try:
        target_file = safe_path(working_directory, file_path)
    except ValueError as e:
        return f'Error: {e}'

    if not target_file.is_file():
        return f'Error: File not found or is not a regular file: {file_path}'
    
    try:
        with target_file.open("r", encoding="utf-8", errors="replace") as f:
            file_content_string = f.read(MAX_CHARS)
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
    except Exception:
        return 'Error: could not read file'

    return file_content_string

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="get contents of a file specified.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="path to the file to read",
            ),
        },
        required=["file_path"]
    ),
)