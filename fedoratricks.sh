#!/bin/bash

set -Eeuo pipefail
trap cleanup SIGINT SIGTERM ERR

# todo - this should be absolute path, depending on where we install the libs, and at the same time it should function in development as structured in this repository.
COMMAND_DIR=commands
COMMANDS=("template" "logs")
args=()

for cmd in "${COMMANDS[@]}" ; do
  source "${COMMAND_DIR}/${cmd}"
done

help() {
  cat <<EOF
Usage: fedoratricks <command> [options]

Global options:
-h|--help   Print the help text and exit.
            Use -h with each command to learn what options they have.

Available commands:
EOF

  for cmd in "${COMMANDS[@]}" ; do
    echo "$cmd"
  done

  if [[ ${#args[@]} != 0 ]]; then
    echo ""

    if [[ ! ${COMMANDS[*]} =~ ${args[0]} ]]; then
      echo "Unknown command: ${args[0]}"
      exit 1
    fi

    ${args[0]}Help
  fi
}

while [[ $# -gt 0 ]]; do
  case $1 in
    -h|--help)
      help
      exit 0
      ;;
    -v|--value)
      exampleValue="$2"
      shift 2
      ;;
    -b|--boolean)
      exampleBool=true
      shift
      ;;
    *)
      args+=("$1")
      shift
      ;;
  esac
done

if [[ ${#args[@]} == 0 ]]; then
  help
  exit 1
fi

if [[ ! ${COMMANDS[*]} =~ ${args[0]} ]]; then
  echo Unknown command.
  exit 1
fi

${args[0]}Execute "${args[@]:1}"

cleanup() {
  trap - SIGINT SIGTERM ERR EXIT
  if [[ ${#args[@]} != 0 ]]; then
    echo ""

    if [[ ! ${COMMANDS[*]} =~ ${args[0]} ]]; then
      ${args[0]}Cleanup
    fi
  fi

}

exit 0
