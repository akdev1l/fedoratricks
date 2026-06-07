from dataclasses import dataclass

@dataclass
class SubcommandArgSpec:
  flags: list[str]
  help: str
  args: dict[str, str]

@dataclass
class SubcommandSpec:
  command: str
  help: str
  args: list[SubcommandArgSpec]
