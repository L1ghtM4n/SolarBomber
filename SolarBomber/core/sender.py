#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author github.com/L1ghtM4n

__all__ = ["request_sender"]

# Import modules
from rich import print
from faker import Faker
from urllib.parse import urljoin
from warnings import filterwarnings
from requests import Session
from requests.exceptions import ConnectTimeout, ReadTimeout
# Import packages
from core.placeholders import replace_placeholders, user_agent

# Ignore warnings
filterwarnings("ignore")


""" Request sender object """
class request_sender(object):
    def __init__(self, phone: str, service: dict, proxies: dict = {}, timeout: int = 1):
        self.phone = phone
        self.service = service
        # Proxy and timeout
        self.proxies = proxies
        self.timeout = timeout
        # Get json, data, params
        self.json = replace_placeholders(phone, service["json"]) if "json" in service else {}
        self.data = replace_placeholders(phone, service["data"]) if "data" in service else {}
        self.params = replace_placeholders(phone, service["params"]) if "params" in service else {}
        # Set default headers
        self.headers = {
            "User-Agent": user_agent,
            "Referer":  urljoin(service["url"], '/'),
            "X-Requested-With": "XMLHttpRequest",
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "Accept-Encoding": "gzip, deflate, br",
        }
        # Set custom headers
        if "headers" in service:
            for hk, hv in service["headers"]:
                self.headers[hk] = hv

    """ Send request to server """
    def send(self) -> bool:
        with Session() as sender_session:
            # Send request to server
            try:
                response = sender_session.request(
                    method="POST", 
                    url=self.service["url"],
                    json=self.json,
                    data=self.data,
                    params=self.params,
                    timeout=self.timeout,
                    proxies=self.proxies,
                    headers=self.headers,
                    verify=False,
                )
            except (ConnectTimeout, ReadTimeout):
                print(f"[red][bold][!][/bold] Connection timed out:[/red] [magenta bold]{self.service['url']}[magenta bold]")
            except Exception as e:
                print(f"[red][bold][!][/bold] Connection error:[/red] [magenta bold]\n{str(e)}[magenta bold]\n")
            else:
                print(f"[cyan][{response.status_code}][/cyan] [green]Request sent to [bold]{self.service['url']}[/bold][/green]\n[yellow]{response.content}[yellow]\n")
                return True
            return False

