import os
import tempfile
import pytest
from corgiTexter import app


@pytest.fixture
def client():

    app.config['TESTING'] = True

# will do testing later, right now this is a placeholder for travis-ci
def test_blank(client):

    return 0