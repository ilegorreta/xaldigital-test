#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from datetime import datetime


def logger(fn):
    def get_current_time():
        now = datetime.now()
        return now.strftime("%d/%m/%Y %H:%M:%S")

    def wrapper():
        dt_string = get_current_time()
        print(f"Starting {fn.__name__} function at: {dt_string}")
        fn()
        dt_string = get_current_time()
        print(f"{fn.__name__} function ended at: {dt_string}")
        return fn

    return wrapper


@logger
def insert_into_postgres():
    try:
        host = "db"
        user = "root"
        password = "password"
        db = "postgres"
        port = "5432"
        engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")
        df = pd.read_csv(f"data/employees.csv")
        df.to_sql(
            con=engine,
            name="employee",
            schema="public",
            if_exists="append",
            index=False,
        )
    except Exception as e:
        print(f"ERROR: {e}")


def state_validation(state):
    if isinstance(state, str) and len(state) == 2:
        return state
    else:
        raise ValueError(f"State value invalid: {state}")


def validate_phone_number(df):
    PHONE_REGEX = "\w{3}-\w{3}-\w{4}"
    if re.search(PHONE_REGEX, df.phone1) and re.search(PHONE_REGEX, df.phone2):
        pass
    else:
        raise ValueError(
            f"Invalid phone number on employee: {df.first_name} {df.last_name}"
        )


def validate_fields():
    df = pd.read_csv(f"data/employees.csv")
    df["state"] = df["state"].apply(lambda x: state_validation(x))
    df.apply(lambda x: validate_phone_number(x), axis=1)


def main():
    validate_fields()
    insert_into_postgres()


if __name__ == "__main__":
    main()
