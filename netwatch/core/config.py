from dataclasses import dataclass, field
from os import getenv
from pathlib import Path

from platformdirs import PlatformDirs

from netwatch.core.watcher import Watcher

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

_PLATFORM_DIRS = PlatformDirs("netwatch", "netwatch")

CONFIG_PATH = Path(getenv("CONFIG_DIR", _PLATFORM_DIRS.user_config_dir)).resolve()
DATA_PATH = Path(getenv("DATA_DIR", _PLATFORM_DIRS.user_data_dir)).resolve()

del _PLATFORM_DIRS

CONFIG_PATH.mkdir(parents=True, exist_ok=True)
DATA_PATH.mkdir(parents=True, exist_ok=True)

NETWATCH_CONFIG_PATH = CONFIG_PATH / "netwatch.yaml"
DATABASE_URL = f"sqlite:///{DATA_PATH / 'netwatch.sqlite3'}"


@dataclass(frozen=True)
class NetwatchConfig:
    watchers: list[Watcher] = field(default_factory=list)
