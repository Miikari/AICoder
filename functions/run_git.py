from pathlib import Path
from google.genai import types
import subprocess
import os

PROJECT_ROOT = Path(__file__).parent.resolve()

ALLOWED_GIT_COMMANDS = {
    "status",
    "diff",
    "add",
    "commit",
    "log",
}

def run_git(working_directory, subcommand, args):
    working_dir_abs = os.path.abspath(working_directory)

    if subcommand not in ALLOWED_GIT_COMMANDS:
        raise ValueError(f"Git subcommand not allowed: {subcommand}")

    cmd = ["git", subcommand, *args]

    result = subprocess.run(
        cmd,
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout + result.stderr


schema_run_git = types.FunctionDeclaration(
    name="run_git",
    description="Run a limited git commands set inside the project repository, commands: ('status', 'diff', 'add', 'commit', 'log').",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "subcommand": types.Schema(
                type=types.Type.STRING,
                description="Git subcommand to run",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="List of arguments to pass to the git subcommand",
                items=types.Schema(type = types.Type.STRING),
            ),
        },
        required=["subcommand", "args"]
    ),
)    