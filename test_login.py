from app import app

import pytest
from flask import url_for
from bs4 import BeautifulSoup
from models import User



@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_login_get(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data


