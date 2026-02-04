# AI agent
Helpful AI agent using Google Gemini 2.5 capable of performing controlled repository operations and local file manipulation via natural-language instructions.

⚠️ Experimental project — use only on non-critical repositories.

Tools available listed:
1. Run, write, read files.
2. List directories and files
3. Stage, commit, and push changes with standardized commit prefixes (5:)
4. Access to internet. (To Be Added)

# Requirements
- Python 3.10+
- uv
- Virtual environment support

# Dependencies
- google.genai
- python-dotenv

# API key
Go to https://aistudio.google.com/ and get api key.
Create .env file and put it here like this:
GEMINI_API_KEY='yourapikeyhere'
REMEMBER TO ADD .env to the .gitignore file, especially when using paid models.. :)

# How to use
Go to the root of project
Activate virtual environment by running: source .venv/bin/activate
Run commands to the agent like this: uv run main.py "Edit a bug in x.py and add, commit and push it to the origin"
AI commits will show up in Git like "5: AI COMMIT ....."

#Constraints - by default
AI has access to the files that are in this project directory.
AI can only handle git commands listed: "status", "diff", "add", "commit", "log", "push"
