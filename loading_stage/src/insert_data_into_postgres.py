#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from datetime import datetime


class CustomException(Exception):
    """Base class for other exceptions regarding XALDIGITAL Data Engineer Test"""

    pass


class PhoneNumberFormatException(CustomException):
    """Raised when there is an issue with the format of a phone number defined in the CSV file"""

    pass


class StateValueException(CustomException):
    """Raised when there is an issue with the value or format of an employee's state defined in the CSV file"""

    pass


def logger(fn):
    def get_current_time():
        now = datetime.now()
        return now.strftime("%d/%m/%Y %H:%M:%S")

    def wrapper(*args, **kwargs):
        dt_string = get_current_time()
        print(f"Starting {fn.__name__} function at: {dt_string}")
        fn(*args, **kwargs)
        dt_string = get_current_time()
        print(f"{fn.__name__} function ended at: {dt_string}")
        return fn

    return wrapper


@logger
def insert_into_postgres(*args, **kwargs):
    try:
        host = os.getenv("POSTGRES_SERVICE_NAME")
        user = os.getenv("POSTGRES_USER")
        password = os.getenv("POSTGRES_PASSWORD")
        db = os.getenv("POSTGRES_DB")
        port = os.getenv("POSTGRES_PORT")
        engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")
        df = args[0]
        df.to_sql(
            con=engine,
            name=os.getenv("TABLE_NAME"),
            schema=os.getenv("POSTGRES_DEFAULT_SCHEMA"),
            if_exists="append",
            index=False,
        )
    except Exception as e:
        print(f"ERROR: {e}")


def state_validation(state):
    if isinstance(state, str) and len(state) == 2:
        return state
    else:
        raise StateValueException(f"State value invalid: {state}")


def validate_phone_number(df):
    PHONE_REGEX = "^\d{3}-\d{3}-\d{4}$"
    if re.search(PHONE_REGEX, df.phone1) and re.search(PHONE_REGEX, df.phone2):
        pass
    else:
        raise PhoneNumberFormatException(
            f"Invalid phone number on employee: {df.first_name} {df.last_name}"
        )


def validate_fields(df):
    df["state"] = df["state"].apply(lambda x: state_validation(x))
    df.apply(lambda x: validate_phone_number(x), axis=1)


def main():
    df = pd.read_csv(f"data/employees.csv")
    validate_fields(df)
    insert_into_postgres(df)


if __name__ == "__main__":
    main()
