#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author github.com/L1ghtM4n

__all__ = ["load_services"]

# Import modules
from os import path
from glob import glob
from time import sleep
from typing import Iterable
from json import load, decoder
from rich import print
from rich.progress import track
from rich.console import Console

# Load bomber services
def load_services(directory: str) -> Iterable[dict]:
    services = glob(path.join(directory, "*.json"))
    # Progress bar
    for service_index in track(range(len(services)), description=f"[bold green]Loading {len(services)} services[/bold green]"):
        json_file = services[service_index]
        # Read json file
        try:
            with open(json_file, 'r', encoding="utf-8", errors="ignore") as obj:
                json_data = load(obj)
        # Handle JSON exception
        except decoder.JSONDecodeError:
            print(f"[red][bold][-][/bold] JSON parsing failed in service:[/red] [magenta bold]{json_file}[/magenta bold]")
        # Handle another exception
        except Exception:
            Console().print_exception(show_locals=True)
            sleep(3)
        # All is okay
        else:
            print(f"[green][+][/green] [yellow bold]Loaded service: {json_file}[/yellow bold]")
            yield json_data
