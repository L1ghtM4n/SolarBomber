#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author github.com/L1ghtM4n

__all__ = ["main"]

# Import modules
from sys import argv
from json import load
from rich import print
from rich.prompt import Prompt
from rich.console import Console
from threading import Thread
from pyfiglet import figlet_format
# Import packages
from core.sender import request_sender
from core.services import load_services


""" Main function """
def main(phone: str, proxies: dict = {}, timeout: int = 1, threads: int = 1) -> int:
    # Load and prepare services
    services = list(map(lambda service: request_sender(
                phone=phone, 
                service=service, 
                proxies=proxies, 
                timeout=timeout
            ), 
            load_services(directory="services")
        ))
    # Create threads for all services
    threads_lists = [[Thread(target=service.send) for service in services] for _ in range(threads)]
    # Start all created threads
    for threads in threads_lists:
        for thread in threads:
            thread.start()
    # Waiting all started threads
    for threads in threads_lists:
        for thread in threads:
            if thread.is_alive():
                thread.join()

    # Exiting
    return 0


if __name__ == "__main__":
    # Print banner
    Console().clear()
    print("[bright_yellow]{0}[/bright_yellow]\t\t[bright_magenta]{1}[/bright_magenta]\n".format(
        figlet_format("SolarBomber", font="slant"),
        "Author : github.com/L1ghtM4n"
    ))
    # Get phone from console
    if len(argv) < 2:
        phone = Prompt.ask("[bold cyan][?][/bold cyan] Please enter target phone number")
    # Get phone from args
    else:
        phone = argv[1]
    # Removing '+' from phone if exists
    phone = phone[1:] if phone[0] == '+' else phone
    # Verify phone number
    if len(phone) < 7 or not phone.isnumeric():
        print(f"[red bold][-][/red bold] [white]Invalid phone number: {phone}[/white]")
        exit(1)
    # Load config
    with open("config.json", 'r') as obj:
        json = load(obj)
    # Parse config
    timeout = json["connection"]["timeout"]
    threads = json["connection"]["threads"]
    proxies = json["connection"]["proxies"]["requests"] if json["connection"]["proxies"]["enabled"] else {}
    # Run main function
    exit(main(phone=phone, proxies=proxies, timeout=timeout, threads=threads))
