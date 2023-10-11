import asyncio
import sys

import hydra
import hydra.core.hydra_config
from omegaconf import DictConfig

from netwatch.core.config import CONFIG_PATH, NetwatchConfig
from netwatch.core.database import get_session


async def amain(cfg: DictConfig):
    config: NetwatchConfig = hydra.utils.instantiate(cfg)
    for watcher in config.watchers:
        with get_session() as session:
            try:
                await watcher.fetch(session)
                session.commit()
            except Exception:
                pass


@hydra.main(
    config_path=str(CONFIG_PATH),
    config_name="netwatch.yaml",
    version_base=None,
)
def main(cfg: DictConfig):
    asyncio.get_event_loop().run_until_complete(amain(cfg))


main()
sys.exit(0)
