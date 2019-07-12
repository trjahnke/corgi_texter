import os
import tempfile
import pytest
from corgiTexter import app


@pytest.fixture
def client():
    
    app.config['TESTING'] = True


def test_empty_db(client):

    return 'nothing'