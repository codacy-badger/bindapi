import json
import time
from copy import deepcopy

import pytest
import responses
from apibank import create_app
from apibank.apibank import BindAPIClient, BindToken
from apibank.helpers import multi_replace_regex
from apibank.url_constants import APIBANK_LOGIN_URL, APIBANK_TX_QUERY_URL, APIBANK_TX_CREATE_URL, APIBANK_ACC_QUERY_URL, \
    APIBANK_DEBIN_CREATE_URL, APIBANK_DEBIN_QUERY_URL
from tests.mocks import APIBANK_TX_QUERY_MOCK, APIBANK_TX_CREATE_MOCK, APIBANK_ACC_QUERY_MOCK, APIBANK_DEBIN_MOCK


@pytest.fixture
def app():
    app = create_app()
    return app

@pytest.fixture
def client(app):
    responses.add(responses.POST,
                  APIBANK_LOGIN_URL,
                  json={'token': 'this-is-a-token', "expires_in": 99999},
                  status=200
                  )
    responses.add(responses.GET,
                  APIBANK_TX_QUERY_URL.replace(":account_id", "21-1-99999-4-6"),
                  json=APIBANK_TX_QUERY_MOCK,
                  status=200
                  )
    responses.add(responses.POST,
                  APIBANK_TX_CREATE_URL.replace(":account_id", "21-1-99999-4-6"),
                  json=APIBANK_TX_CREATE_MOCK,
                  status=200
                  )
    APIBANK_TX_CREATE_MOCK_W_ERROR = deepcopy(APIBANK_TX_CREATE_MOCK)
    APIBANK_TX_CREATE_MOCK_W_ERROR["status"] = "ERROR"
    responses.add(responses.POST,
                  APIBANK_TX_CREATE_URL.replace(":account_id", "21-1-99999-4-6"),
                  json=APIBANK_TX_CREATE_MOCK_W_ERROR,
                  status=200
                  )


    return app.test_client()

@responses.activate
def test_get_transfers(client):
    response = client.get("/transfers")
    assert response.status_code == 200
    assert len(response.json) == 1
    assert len(response.json[0]) == 4
    assert response.json[0]["id"] == APIBANK_TX_QUERY_MOCK[0]["id"]
    assert response.json[0]["cuil"] == APIBANK_TX_QUERY_MOCK[0]["counterparty"]["id"]
    assert response.json[0]["amount"] == APIBANK_TX_QUERY_MOCK[0]["charge"]["value"]["amount"]
    assert response.json[0]["currency"] == APIBANK_TX_QUERY_MOCK[0]["charge"]["value"]["currency"]

@responses.activate
def test_make_transfer(client):
    json_body = {
        "cbu": "0074256415652456325214",
        "amount": "10000",
        "currency": "ARS"
    }

    response = client.post("/transfer", json=json_body)
    assert response.status_code == 200
    assert response.json["message"] == "Transferencia exitosa"

    # same transfer but with an error
    response = client.post("/transfer", json=json_body)
    assert response.status_code == 200
    assert response.json["message"] == "Transferencia rechazada"


@responses.activate
def test_account_detail_by_cbu(client):
    query_params = {
        ":account_type": "cbu",
        ":account_nro": "0074256415652456325214"
    }

    json_body = {
        "cbu": "0074256415652456325214"
    }
    with responses.RequestsMock() as rsps:
        rsps.add(responses.GET,
                  multi_replace_regex(APIBANK_ACC_QUERY_URL, query_params),
                  json=APIBANK_ACC_QUERY_MOCK,
                  status=200
                  )
        response = client.post("/account_details", json=json_body)
        assert response.status_code == 200
        assert len(response.json) == 6
        assert response.json["cbu"] == APIBANK_ACC_QUERY_MOCK["account_routing"]["address"]
        assert response.json["alias"] == ""
        assert response.json["currency"] == APIBANK_ACC_QUERY_MOCK["currency"]
        assert response.json["cuil"] == APIBANK_ACC_QUERY_MOCK["owners"][0]["id"]
        assert response.json["bank_name"] == APIBANK_ACC_QUERY_MOCK["bank_routing"]["address"]
        assert response.json["fullname"] == APIBANK_ACC_QUERY_MOCK["owners"][0]["display_name"]

@responses.activate
def test_account_detail_by_alias(client):
    query_params = {
        ":account_type": "alias",
        ":account_nro": "MIALIAS"
    }

    json_body = {
        "alias": "MIALIAS"
    }

    with responses.RequestsMock() as rsps:
        rsps.add(responses.GET,
                  multi_replace_regex(APIBANK_ACC_QUERY_URL, query_params),
                  json=APIBANK_ACC_QUERY_MOCK,
                  status=200
                  )
        response = client.post("/account_details", json=json_body)
        assert response.status_code == 200
        assert len(response.json) == 6
        assert response.status_code == 200
        assert len(response.json) == 6
        assert response.json["cbu"] == APIBANK_ACC_QUERY_MOCK["account_routing"]["address"]
        assert response.json["alias"] == ""
        assert response.json["currency"] == APIBANK_ACC_QUERY_MOCK["currency"]
        assert response.json["cuil"] == APIBANK_ACC_QUERY_MOCK["owners"][0]["id"]
        assert response.json["bank_name"] == APIBANK_ACC_QUERY_MOCK["bank_routing"]["address"]
        assert response.json["fullname"] == APIBANK_ACC_QUERY_MOCK["owners"][0]["display_name"]


@responses.activate
def test_make_debin(client):
    json_body = {
        "cbu": "3220001801000020816200",
        "amount": "444",
        "currency": "ARS"
    }
    with responses.RequestsMock() as rsps:
        rsps.add(responses.POST,
                 APIBANK_DEBIN_CREATE_URL.replace(":account_id", "21-1-99999-4-6"),
                 json=APIBANK_DEBIN_MOCK,
                 status=200
                 )
        response = client.post("/debin", json=json_body)
        assert response.status_code == 200
        assert response.json["message"] == "Pedido de DEBIN creado"

@responses.activate
def test_make_debin_w_error(client):
    json_body = {
        "cbu": "3220001801000020816200",
        "amount": "444",
        "currency": "ARS"
    }

    with responses.RequestsMock() as rsps:
        APIBANK_DEBIN_MOCK["status"] = "ERROR"
        rsps.add(responses.POST,
                 APIBANK_DEBIN_CREATE_URL.replace(":account_id", "21-1-99999-4-6"),
                 json=APIBANK_DEBIN_MOCK,
                 status=200
                 )
        response = client.post("/debin", json=json_body)
        assert response.status_code == 200
        assert response.json["message"] == "Pedido de DEBIN NO creado"


@responses.activate
def test_get_debin(client):
    query_params = {
        ":account_id": "21-1-99999-4-6",
        ":transaction_id": "JMRD06ZO9WX5Z125GP7XY3"
    }

    json_body = {
        "id": "JMRD06ZO9WX5Z125GP7XY3"
    }

    with responses.RequestsMock() as rsps:
        APIBANK_DEBIN_MOCK["status"] = "COMPLETED"
        rsps.add(responses.GET,
                 multi_replace_regex(APIBANK_DEBIN_QUERY_URL, query_params),
                 json=APIBANK_DEBIN_MOCK,
                 status=200
                 )
        response = client.get("/debin", json=json_body)
        assert response.status_code == 200
        assert response.json["completed"] == True

@responses.activate
def test_get_debin_w_errors(client):
    query_params = {
        ":account_id": "21-1-99999-4-6",
        ":transaction_id": "JMRD06ZO9WX5Z125GP7XY3"
    }

    json_body = {
        "id": "JMRD06ZO9WX5Z125GP7XY3"
    }

    with responses.RequestsMock() as rsps:
        APIBANK_DEBIN_MOCK["status"] = "ERROR"
        rsps.add(responses.GET,
                 multi_replace_regex(APIBANK_DEBIN_QUERY_URL, query_params),
                 json=APIBANK_DEBIN_MOCK,
                 status=200
                 )
        response = client.get("/debin", json=json_body)
        assert response.status_code == 200
        assert response.json["completed"] == False

def test_parse_handle_error():
    client = BindAPIClient()

    class customResponse:
        status_code = 200

        def json(self):
            return {"code": "XXXX", "message": "This is an error." }

    custom_response = customResponse()

    response = client.handle_response(custom_response, url_to_parse="http://wrong_url.com")
    assert response["message"] == "Invalid url"

    custom_response.status_code = 400
    with pytest.raises(Exception):
        client.handle_response(custom_response, url_to_parse="http://wrong_url.com")

def test_build_token_error():
    client = BindAPIClient()
    with responses.RequestsMock() as rsps:
        rsps.add(responses.POST,
                 APIBANK_LOGIN_URL,
                 json={"code": "GE500", "message": "Could not resolve request message body"},
                 status=400
                 )
        with pytest.raises(Exception):
            client.build_token()

def test_app_alive(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.data == b"Hello World!"

def test_token_expiration(client):
    token = BindToken({"expires_in":-1, "token": "XXXXXXXX"})
    with pytest.raises(Exception):
        token.auth_header()
