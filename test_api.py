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

def test_prediction_100002():
    expected_value = 0.98
    assert api.prediction(100002) <= expected_value

def test_prediction_100003():
    expected_value = 0.05
    assert api.prediction(100003) >= expected_value

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

def test_make_feats_first_feat_100002():
    expected_value = "EXT_SOURCE_3"
    assert expected_value in api.make_feats(100002)

def test_make_feats_len_dict_100003():
    expected_value = 10
    assert len(api.make_feats(100003)) == expected_value

