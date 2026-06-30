import argparse
import logging
import sys
from pathlib import Path

import fedoratricks.plugins as plugins
from .cli_spec import SubcommandArgSpec, SubcommandSpec

def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s:%(lineno)d > %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    plugin_list = [
      # plugins.template,
      plugins.nvidia,
      plugins.rpmfusion,
      plugins.codecs,
    ]

    program_name = Path(sys.argv[0]).name
    command_parser = argparse.ArgumentParser(
        prog=program_name,
        description="Fedora tips and tricks CLI",
    )
    subcommand_parsers = command_parser.add_subparsers()

    for plugin in plugin_list:
      subcommand = plugin.subcommand_spec
      subparser = subcommand_parsers.add_parser(subcommand.command, help=subcommand.help)
      subparser.set_defaults(plugin=plugin)

      for arg_spec in subcommand.args:
        flags = arg_spec.flags
        subparser.add_argument(
          flags[0],
          flags[1],
          help=arg_spec.help,
          **arg_spec.args,
        )


    command_parser.add_argument("--version", action="version", version="%(prog)s 0.1.0")
    args = command_parser.parse_args()

    plugin = getattr(args, "plugin", None)
    if plugin is None:
      command_parser.print_help()
      return

    plugin.apply(args)


if __name__ == "__main__":
    sys.exit(main())
