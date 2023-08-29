import sqlite3 as sql
import pytest
from main import get_pokemon
from main import get_berries
from main import app, remove_from_cart, get_cart
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

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    yield client

def test_remove_from_cart(client):
    with client:
        response = client.post('/add-to-cart', data={
            'item_id': 1,
            'item_type': 'pokemon',
            'item_name': 'Pikachu'
        })
        assert response.status_code == 302

    with client:
        response = client.post('/remove_from_cart/1')
        assert response.status_code == 302  

    cart = get_cart()
    assert 1 not in [item['ID'] for item in cart]
