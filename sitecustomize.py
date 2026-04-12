from rich.console import Console
from rich.traceback import install

install(show_locals=True, width=120, console=Console(force_terminal=True))
