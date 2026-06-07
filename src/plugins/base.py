from abc import ABC, abstractmethod

class PluginBase(ABC):
  subcommand_spec: SubcommandSpec

  @abstractmethod
  def apply(self, argv):
    pass

