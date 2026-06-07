from .template import TemplatePlugin
from .nvidia import NvidiaPlugin
from .rpmfusion import RpmFusionPlugin
from .codecs import CodecsPlugin

template = TemplatePlugin()
nvidia = NvidiaPlugin()
rpmfusion = RpmFusionPlugin()
codecs = CodecsPlugin()

__all__ = [
  "codecs",
  "rpmfusion",
  "template",
  "nvidia",
]
