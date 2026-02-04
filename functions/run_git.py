from pathlib import Path
from google.genai import types
import subprocess
import os

PROJECT_ROOT = Path(__file__).parent.parent.resolve()

ALLOWED_GIT_COMMANDS = {
    "status",
    "diff",
    "add",
    "commit",
    "log",
    "push"
}

def run_git(working_directory, subcommand, args):
    working_dir_abs = PROJECT_ROOT

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
                description="Git subcommand to run. Always check log which was the starting message and increment it for the next commit and add 'AI Commit' for exmaple if last commit message was '4: Did this' Your next commit message is '5: AI commit, did this'",
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