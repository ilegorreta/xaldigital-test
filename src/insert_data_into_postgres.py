#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psycopg2
import os
import pandas as pd
from sqlalchemy import create_engine


def main():
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


if __name__ == "__main__":
    print("Inserting into Postgres...")
    main()
    print("Inserted successfully!")
