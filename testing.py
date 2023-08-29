import sqlite3 as sql
import pytest
from main import get_pokemon
from main import get_berries


def test_get_pokemon():
    # Setup
    # You might need to create a temporary database with test data for this test

    # Exercise
    result = get_pokemon()

    # Verify
    assert isinstance(result, list)
    assert len(result) > 0
    # Add more assertions based on the expected behavior of get_pokemon()

def test_get_berries():

    result = get_berries()
    assert isinstance(result, list)
    assert len(result) > 0




# If you want to run the tests directly when the script is executed

