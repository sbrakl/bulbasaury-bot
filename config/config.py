import inspect
import os
from pathlib import Path
from dotenv import load_dotenv

# Configuration setting for the bot

def loadConf():
    stack = inspect.stack()
    calling_context = next(context for context in stack if context.filename != __file__)
    root_dir = os.path.dirname(calling_context.filename)
    env_path = Path(root_dir) / '.env'
    if os.path.exists(env_path):
        load_dotenv(dotenv_path=env_path)
    else:
        raise FileNotFoundError('.env file is require at root of the project which contains all secrets loaded by application')