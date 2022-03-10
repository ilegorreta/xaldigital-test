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
        df["employee_id"] = df.index + 1
        # shift column 'employee_id' to first position
        first_column = df.pop("employee_id")
        df.insert(0, "employee_id", first_column)
        df.to_sql(con=engine, name="employee", if_exists="replace", index=False)
    except Exception as e:
        print(f"ERROR: {e}")


if __name__ == "__main__":
    print("Inserting into Postgres...")
    main()
    print("Inserted successfully!")
