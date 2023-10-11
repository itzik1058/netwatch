import asyncio
import sys

from hydra.utils import instantiate
from omegaconf import OmegaConf

from netwatch.core.config import NETWATCH_CONFIG_PATH, NetwatchConfig
from netwatch.core.database import get_session


async def main():
    config: NetwatchConfig = instantiate(OmegaConf.load(NETWATCH_CONFIG_PATH))
    while True:
        for watcher in config.watchers:
            with get_session() as session:
                try:
                    await watcher.fetch(session)
                    session.commit()
                except Exception:
                    pass
        await asyncio.sleep(180)


asyncio.get_event_loop().run_until_complete(main())
sys.exit(0)
