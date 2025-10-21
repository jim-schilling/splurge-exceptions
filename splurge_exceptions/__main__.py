"""Enable running the package as a module with: python -m splurge_exceptions"""

import sys

from splurge_exceptions.cli import main

if __name__ == "__main__":
    sys.exit(main())
