from ..cli_spec import SubcommandArgSpec, SubcommandSpec
from .base import PluginBase
from logging import getLogger

logger = getLogger(__name__)


class NvidiaPlugin(PluginBase):

  def __init__(self):
    self.subcommand_spec = SubcommandSpec(
      command="nvidia",
      help="configure nvidia drivers",
      args=[
        SubcommandArgSpec(
          flags=["-y", "--yes"],
          help="assume yes to any prompts",
          args={
            "action": "store_true",
          },
        ),
      ],
    )

  def apply(self, argv):
    logger.info("configuring nvidia driver")
