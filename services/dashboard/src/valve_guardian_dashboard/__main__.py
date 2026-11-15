import sys
from pathlib import Path
from typing import Final

from streamlit.web import cli

PAGE: Final = Path(__file__).with_name("app.py")
OPTIONS: Final = (
    "--browser.gatherUsageStats=false",
    "--server.headless=true",
    "--client.toolbarMode=minimal",
    "--server.address=127.0.0.1",
    "--browser.serverAddress=localhost",
)


def main() -> None:
    """Run the page; extra arguments are streamlit options, the last one wins."""
    sys.argv = ["streamlit", "run", *OPTIONS, *sys.argv[1:], str(PAGE)]
    sys.exit(cli.main())


if __name__ == "__main__":
    main()
