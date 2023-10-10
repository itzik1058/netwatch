from os import getenv
from pathlib import Path

from platformdirs import user_data_dir

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

DATA_PATH = Path(getenv("DATA_PATH", user_data_dir("netwatch", "netwatch")))
DATA_PATH.mkdir(parents=True, exist_ok=True)
DATABASE_URL = getenv("DATABASE_URL", f"sqlite:///{DATA_PATH}/netwatch.sqlite3")
