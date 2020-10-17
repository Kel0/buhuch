"""
Settings
~~~~~~~~

This module load .env file's vars and store the const variables
"""
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()
load_dotenv(verbose=True)
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

BILLS_SITE_URL = str(os.getenv("BILLS_LINK"))
HEADERS = {
    "accept": "*/*",
    "user-agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
    )
}
BASE_DIR = Path(__file__).resolve().parent
