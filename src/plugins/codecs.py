import subprocess
from ..cli_spec import SubcommandArgSpec, SubcommandSpec
from .base import PluginBase
from logging import getLogger

logger = getLogger(__name__)

GPU_VENDOR_PACKAGES = {
  "intel": ["intel-media-driver"],
  "amd": ["mesa-va-drivers-freeworld", "mesa-va-drivers-freeworld.i686"],
  "nvidia": ["libva-nvidia-driver", "libva-nvidia-driver.i686"],
}


class CodecsPlugin(PluginBase):
  """
  Automates the process documented in: https://rpmfusion.org/Howto/Multimedia

  sudo dnf swap ffmpeg-free ffmpeg --allowerasing
  sudo dnf update @multimedia --setopt="install_weak_deps=False" --exclude=PackageKit-gstreamer-plugin

  # If Intel:
  sudo dnf install intel-media-driver

  # If AMD(Mesa):
  sudo dnf install mesa-va-drivers-freeworld
  sudo dnf install mesa-va-drivers-freeworld.i686

  # If Nvidia:
  sudo dnf install libva-nvidia-driver
  sudo dnf install libva-nvidia-driver.i686

  # For DVD playing:
  sudo dnf install libdvdcss
  """

  def __init__(self):
    self.subcommand_spec = SubcommandSpec(
      command="codecs",
      help="configure proprietary codec support",
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
    self._swap_ffmpeg(argv)
    self._update_multimedia_group(argv)
    self._install_hardware_codecs(argv)
    self._dnf_install(argv, "libdvdcss")

  def _swap_ffmpeg(self, argv):
    if self._is_installed("ffmpeg"):
      logger.info("ffmpeg is already installed, skipping swap")
      return

    logger.info("swapping ffmpeg-free for ffmpeg")
    self._run_dnf(argv, ["swap", "ffmpeg-free", "ffmpeg", "--allowerasing"])

  def _update_multimedia_group(self, argv):
    logger.info("updating multimedia group")
    self._run_dnf(argv, [
      "update", "@multimedia",
      "--setopt=install_weak_deps=False",
      "--exclude=PackageKit-gstreamer-plugin",
    ])

  def _install_hardware_codecs(self, argv):
    vendors = self._detect_gpu_vendors()
    if not vendors:
      logger.warning("could not detect a supported gpu vendor, skipping hardware codec install")
      return

    for vendor in vendors:
      self._dnf_install(argv, *GPU_VENDOR_PACKAGES[vendor])

  def _detect_gpu_vendors(self):
    output = subprocess.run(
      ["lspci"], capture_output=True, text=True, check=True,
    ).stdout.lower()

    gpu_lines = [
      line for line in output.splitlines()
      if "vga" in line or "3d controller" in line or "display controller" in line
    ]

    vendors = set()
    for line in gpu_lines:
      for vendor in GPU_VENDOR_PACKAGES:
        if vendor in line or (vendor == "amd" and "ati" in line):
          vendors.add(vendor)

    return vendors

  def _dnf_install(self, argv, *packages):
    missing = [package for package in packages if not self._is_installed(package)]
    if not missing:
      logger.info("already installed, skipping: %s", ", ".join(packages))
      return

    logger.info("installing: %s", ", ".join(missing))
    self._run_dnf(argv, ["install", *missing])

  def _run_dnf(self, argv, dnf_args):
    command = ["sudo", "dnf", *dnf_args]
    if argv.yes:
      command.append("-y")
    subprocess.run(command, check=True)

  def _is_installed(self, package):
    return subprocess.run(
      ["rpm", "-q", package],
      stdout=subprocess.DEVNULL,
      stderr=subprocess.DEVNULL,
    ).returncode == 0
