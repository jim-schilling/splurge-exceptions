"""Command-line interface for Splurge Exceptions.

Provides CLI commands for the Splurge Exceptions framework.
"""

import argparse
import sys

from splurge_exceptions import __version__


def main(args: list[str] | None = None) -> int:
    """Main CLI entry point.

    Args:
        args: Command-line arguments (defaults to sys.argv[1:])

    Returns:
        Exit code (0 for success, 1+ for errors)
    """
    parser = argparse.ArgumentParser(
        prog="splurge-exceptions",
        description="Splurge Exceptions - Python exception framework",
    )

    # Global version argument
    parser.add_argument(
        "--version",
        action="version",
        version=f"splurge-exceptions {__version__}",
    )

    # Parse arguments (validates syntax)
    parser.parse_args(args)

    # If no command specified, show help
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
