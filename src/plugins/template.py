from ..cli_spec import SubcommandArgSpec, SubcommandSpec
from .base import PluginBase
from logging import getLogger

logger = getLogger(__name__)


class TemplatePlugin(PluginBase):

  def __init__(self):
    self.subcommand_spec = SubcommandSpec(
      command="template",
      help="template plugin",
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
    logger.info("apply with args: %s", argv)
