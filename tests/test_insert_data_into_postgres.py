#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import pytest
import pandas as pd

script_dir = os.path.dirname(__file__)
mymodule_dir = os.path.join(script_dir, "..", "loading_stage", "src")
sys.path.append(mymodule_dir)
import insert_data_into_postgres


@pytest.fixture
def data_path():
    TEST_SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
    DATA_PATH = f"{TEST_SCRIPT_PATH}/test_data"
    return DATA_PATH


def test_raises_phone1_format_error(data_path):
    """Raises a PhoneNumberFormatException"""
    df = pd.read_csv(f"{data_path}/invalid_phone1_format.csv")
    with pytest.raises(insert_data_into_postgres.PhoneNumberFormatException):
        insert_data_into_postgres.validate_fields(df)


def test_raises_phone2_format_error(data_path):
    """Raises a PhoneNumberFormatException"""
    df = pd.read_csv(f"{data_path}/invalid_phone2_format.csv")
    with pytest.raises(insert_data_into_postgres.PhoneNumberFormatException):
        insert_data_into_postgres.validate_fields(df)


def test_raises_state_error(data_path):
    """Raises a StateValueException"""
    df = pd.read_csv(f"{data_path}/invalid_state.csv")
    with pytest.raises(insert_data_into_postgres.StateValueException):
        insert_data_into_postgres.validate_fields(df)


def test_insert(data_path):
    """Test the correct insertion to Postgres"""
    df = pd.read_csv(f"{data_path}/valid_insert.csv")
    insert_data_into_postgres.insert_into_postgres(df)
