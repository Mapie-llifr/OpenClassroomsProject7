import pytest
from OpenClassroomsProject7 import api

"""
@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    clear_all()
    with app.test_client() as client:
        yield client
        
@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield app

#@pytest.fixture
#def app():
#    api = Flask(__name__)
#    api.config({'TESTING':True})
#    yield api
"""
SEUIL = 0.2



def test_accord_accorded():
    pred = 0.1
    expected_value = 1
    assert api.accord(pred) == expected_value

def test_accord_risked():
    pred = 0.3
    expected_value = 5
    assert api.accord(pred) == expected_value

def test_accord_refused():
    pred = 0.8
    expected_value = 0
    assert api.accord(pred) == expected_value