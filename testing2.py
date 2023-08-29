import pytest
from main import app, remove_from_cart, get_cart

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    yield client

def test_remove_from_cart(client):
    # Simulate adding an item to the cart for testing purposes
    with client:
        response = client.post('/add-to-cart', data={
            'item_id': 1,
            'item_type': 'pokemon',
            'item_name': 'Pikachu'
        })
        assert response.status_code == 302  # Check that the item was added successfully

    # Simulate removing the item from the cart
    with client:
        response = client.post('/remove_from_cart/1')
        assert response.status_code == 302  # Check that the item was removed successfully

    # Check that the item is not in the cart anymore
    cart = get_cart()
    assert 1 not in [item['ID'] for item in cart]

