#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author github.com/L1ghtM4n

__all__ = ["replace_placeholders", "user_agent"]

# Import modules
from faker import Faker

# Init faker
faker = Faker()
# Generate random user agent
user_agent = faker.user_agent()

""" Replace values in request data """
def replace_placeholders(phone: str, data: dict) -> dict:
    # Replace map
    replace_map = {
        "$phone": lambda: phone,
        "$username": faker.user_name,
        "$password": faker.password,
        "$firstname": faker.first_name,
        "$lastname": faker.last_name,
        "$fullname": faker.name,
        "$job": faker.job,
        "$email": faker.free_email,
        "$country": faker.country,
        "$street_address": faker.street_address,
        "$credit_card_number": faker.credit_card_number,
        "$credit_card_provider": faker.credit_card_provider,
        "$credit_card_security_code": faker.credit_card_security_code,
    }.items()
    # Replace data
    for dk, dv in data.items():
        for rk, rv in replace_map:
            if type(dv) == str and rk in dv:
                data[dk] = dv.replace(rk, rv())
    return data

