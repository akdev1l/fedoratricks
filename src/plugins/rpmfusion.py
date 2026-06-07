import subprocess
from ..cli_spec import SubcommandArgSpec, SubcommandSpec
from .base import PluginBase
from logging import getLogger

logger = getLogger(__name__)

RPMFUSION_PACKAGES = ["rpmfusion-free-release", "rpmfusion-nonfree-release"]


class RpmFusionPlugin(PluginBase):

  def __init__(self):
    self.subcommand_spec = SubcommandSpec(
      command="rpmfusion",
      help="configure rpmfusion repository",
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
    if self._is_installed():
      logger.info("rpmfusion repositories are already configured")
      return

    fedora_version = subprocess.run(
      ["rpm", "-E", "%fedora"],
      capture_output=True,
      text=True,
      check=True,
    ).stdout.strip()

    urls = [
      f"https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-{fedora_version}.noarch.rpm",
      f"https://mirrors.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-{fedora_version}.noarch.rpm",
    ]

    command = ["sudo", "dnf", "install"]
    if argv.yes:
      command.append("-y")
    command.extend(urls)

    logger.info("installing rpmfusion repositories")
    subprocess.run(command, check=True)

  def _is_installed(self):
    result = subprocess.run(
      ["rpm", "-q", *RPMFUSION_PACKAGES],
      stdout=subprocess.DEVNULL,
      stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0
