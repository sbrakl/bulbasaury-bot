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
    load_dotenv(dotenv_path=env_path)