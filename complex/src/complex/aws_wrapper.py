"""Complex CLI."""

import os
import sys

from awscli import clidriver


def awscli() -> None:
    """AWS CLI."""
    if os.environ.get("LC_CTYPE", "") == "UTF-8":
        os.environ["LC_CTYPE"] = "en_US.UTF-8"
    return sys.exit(clidriver.main())
