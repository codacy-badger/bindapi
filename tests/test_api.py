from copy import deepcopy

import pytest
import responses
from apibank import create_app
from apibank.apibank import BindAPIClient, BindToken
from apibank.helpers import multi_replace_regex
from apibank.url_constants import APIBANK_LOGIN_URL, APIBANK_TX_QUERY_URL, APIBANK_TX_CREATE_URL, \
    APIBANK_ACC_QUERY_URL, APIBANK_DEBIN_CREATE_URL, APIBANK_DEBIN_QUERY_URL, APIBANK_DEBIN_SUBSCRIPTION_CREATE_URL, \
    APIBANK_DEBIN_SUBSCRIPTION_QUERY_URL
from tests.mocks import APIBANK_TX_QUERY_MOCK, APIBANK_TX_CREATE_MOCK, APIBANK_ACC_QUERY_MOCK, APIBANK_DEBIN_MOCK, \
    APIBANK_DEBIN_SUBSCRIPTION_MOCK


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
                  APIBANK_TX_QUERY_URL,
                  json=APIBANK_TX_QUERY_MOCK,
                  status=200
                  )

    mock_w_error = deepcopy(APIBANK_TX_CREATE_MOCK)
    mock_w_error["status"] = "ERROR"
    responses.add(responses.POST,
                  APIBANK_TX_CREATE_URL,
                  json=mock_w_error,
                  status=200
                  )

    return app.test_client()


@responses.activate
def test_get_transfers(client):
    response = client.get("/transfers")
    assert response.status_code == 200
    assert len(response.json) == 1
    assert len(response.json[0]) == 11
    assert response.json[0]["id"] == APIBANK_TX_QUERY_MOCK[0]["id"]
    assert response.json[0]["counterparty"]["id"] == APIBANK_TX_QUERY_MOCK[0]["counterparty"]["id"]
    assert response.json[0]["charge"]["value"]["amount"] == APIBANK_TX_QUERY_MOCK[0]["charge"]["value"]["amount"]
    assert response.json[0]["charge"]["value"]["currency"] == APIBANK_TX_QUERY_MOCK[0]["charge"]["value"]["currency"]


@responses.activate
def test_make_transfer(client):
    json_body = {
        "cbu": "0074256415652456325214",
        "amount": "10000",
        "currency": "ARS"
    }
    with responses.RequestsMock() as rsps:
        APIBANK_TX_CREATE_MOCK["charge"]["value"]["amount"] = json_body["amount"]
        rsps.add(responses.POST,
                 APIBANK_TX_CREATE_URL,
                 json=APIBANK_TX_CREATE_MOCK,
                 status=200
                 )
        response = client.post("/transfer", json=json_body)
        assert response.status_code == 200
        assert len(response.json) == 11
        assert response.json["id"] == APIBANK_TX_CREATE_MOCK["id"]
        assert response.json["status"] == "COMPLETED"
        assert response.json["status"] == APIBANK_TX_CREATE_MOCK["status"]
        assert response.json["charge"]["summary"] == "COMPLETE_TRANS"
        assert response.json["charge"]["summary"] == APIBANK_TX_CREATE_MOCK["charge"]["summary"]
        assert response.json["charge"]["value"]["amount"] == APIBANK_TX_CREATE_MOCK["charge"]["value"]["amount"]
        assert response.json["charge"]["value"]["amount"] == json_body["amount"]


@responses.activate
def test_make_transfer_w_error(client):
    json_body = {
        "cbu": "0074256415652456325214",
        "amount": "10000",
        "currency": "XXX"
    }
    with responses.RequestsMock() as rsps:
        mock_w_error = {"code": "GE500", "message": "Could not resolve request message body"}

        rsps.add(responses.POST,
                 APIBANK_TX_CREATE_URL,
                 json=mock_w_error,
                 status=400
                 )
        response = client.post("/transfer", json=json_body)
        assert response.status_code == 200
        assert response.json["code"] == mock_w_error["code"]
        assert response.json["message"] == mock_w_error["message"]


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
        assert len(response.json) == 7
        assert response.json["account_routing"]["address"] == APIBANK_ACC_QUERY_MOCK["account_routing"]["address"]
        assert response.json["currency"] == APIBANK_ACC_QUERY_MOCK["currency"]
        assert response.json["owners"][0]["id"] == APIBANK_ACC_QUERY_MOCK["owners"][0]["id"]
        assert response.json["label"] == APIBANK_ACC_QUERY_MOCK["label"]
        assert len(response.json["bank_routing"]) == 3
        assert len(response.json["account_routing"]) == 2


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
        assert len(response.json) == 7
        assert response.json["account_routing"]["address"] == APIBANK_ACC_QUERY_MOCK["account_routing"]["address"]
        assert response.json["currency"] == APIBANK_ACC_QUERY_MOCK["currency"]
        assert response.json["owners"][0]["id"] == APIBANK_ACC_QUERY_MOCK["owners"][0]["id"]
        assert response.json["label"] == APIBANK_ACC_QUERY_MOCK["label"]
        assert len(response.json["bank_routing"]) == 3
        assert len(response.json["account_routing"]) == 2


@responses.activate
def test_make_debin(client):
    json_body = {
        "cbu": "3220001801000020816200",
        "amount": "444",
        "currency": "ARS"
    }
    with responses.RequestsMock() as rsps:
        rsps.add(responses.POST,
                 APIBANK_DEBIN_CREATE_URL,
                 json=APIBANK_DEBIN_MOCK,
                 status=200
                 )
        response = client.post("/debin", json=json_body)
        assert response.status_code == 200
        assert len(response.json) == 11
        assert response.json["status"] == APIBANK_DEBIN_MOCK["status"]
        assert response.json["status_description"] == APIBANK_DEBIN_MOCK["status_description"]
        assert len(response.json["transaction_ids"]) == 1
        assert response.json["status"] == APIBANK_DEBIN_MOCK["status"]


@responses.activate
def test_make_debin_w_error(client):
    json_body = {
        "cbu": "3220001801000020816200",
        "amount": "444",
        "currency": "ARS"
    }

    with responses.RequestsMock() as rsps:
        mock_w_error = {"code": "GE500", "message": "Could not resolve request message body"}
        rsps.add(responses.POST,
                 APIBANK_DEBIN_CREATE_URL,
                 json=mock_w_error,
                 status=409
                 )
        response = client.post("/debin", json=json_body)
        assert response.status_code == 200
        assert response.json["code"] == mock_w_error["code"]
        assert response.json["message"] == mock_w_error["message"]


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
        assert len(response.json) == 11
        assert response.json["status"] == APIBANK_DEBIN_MOCK["status"]
        assert response.json["status"] == "COMPLETED"
        assert response.json["status_description"] == APIBANK_DEBIN_MOCK["status_description"]
        assert len(response.json["transaction_ids"]) == 1
        assert response.json["status"] == APIBANK_DEBIN_MOCK["status"]


@responses.activate
def test_get_debin_w_errors(client):
    json_body = {
        "id": "JMRD06ZO9WX5Z125GP7XY3"
    }

    with responses.RequestsMock() as rsps:
        mock_w_error = {"code": "GE500", "message": "Could not resolve request message body"}
        rsps.add(responses.GET,
                 APIBANK_DEBIN_QUERY_URL.replace(":transaction_id", "JMRD06ZO9WX5Z125GP7XY3"),
                 json=mock_w_error,
                 status=200
                 )
        response = client.get("/debin", json=json_body)
        assert response.status_code == 200
        assert response.json["code"] == mock_w_error["code"]
        assert response.json["message"] == mock_w_error["message"]


def test_parse_handle_error():
    client = BindAPIClient()

    class CustomResponse:
        status_code = 200

        def json(self):
            return {"code": "XXXX", "message": "This is an error."}

    custom_response = CustomResponse()

    response = client.handle_response(custom_response, url_to_parse="http://wrong_url.com")
    custom_response.status_code = 200
    assert response["code"] == custom_response.json()["code"]
    assert response["message"] == custom_response.json()["message"]


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
    token = BindToken({"expires_in": -1, "token": "XXXXXXXX"})
    with pytest.raises(Exception):
        token.auth_header()


@responses.activate
def test_create_debin_subscription(client):
    json_body = {
        "account_type": "alias",
        "account_nro": "aliasCBU",
        "description": "description here",
        "provision": "provision here",
        "provision_reference": "provision_reference here"
    }

    with responses.RequestsMock() as rsps:
        rsps.add(responses.POST,
                 APIBANK_DEBIN_SUBSCRIPTION_CREATE_URL,
                 json=APIBANK_DEBIN_SUBSCRIPTION_MOCK,
                 status=200
                 )
        response = client.post("/debin-subscription", json=json_body)
        assert response.status_code == 200
        assert len(response.json) == 9
        assert len(response.json["transaction_ids"]) == 2


@responses.activate
def test_create_debin_subscription_w_accounttype_error(client):
    json_body = {
        "account_type": "WRONG-ACCOUNT-TYPE",
        "account_nro": "aliasCBU",
        "description": "description here",
        "provision": "provision here",
        "provision_reference": "provision_reference here"
    }

    response = client.post("/debin-subscription", json=json_body)
    assert response.status_code == 200
    assert response.json["code"] == "ER001"
    assert response.json["message"] == "Invalid account_type. Check your request parameters."


@responses.activate
def test_create_debin_subscription_w_param_error(client):
    json_body = {
        "account_type": "alias",
        "account_nro": "aliasCBU",
        "provision": "provision here",
        "provision_reference": "provision_reference here"
    }

    response = client.post("/debin-subscription", json=json_body)
    assert response.status_code == 200
    assert response.json["code"] == "ER001"
    assert response.json["message"] == "Missing mandatory parameters. Check your request parameters."


@responses.activate
def test_get_debin_subscription(client):
    json_body = {
        "transaction_id": "0"
    }

    with responses.RequestsMock() as rsps:

        rsps.add(responses.GET,
                 APIBANK_DEBIN_SUBSCRIPTION_QUERY_URL.replace(":transaction_id", json_body["transaction_id"]),
                 json=APIBANK_DEBIN_SUBSCRIPTION_MOCK,
                 status=200
                 )
        response = client.get("/debin-subscription", json=json_body)
        assert response.status_code == 200
        assert len(response.json) == 9
        assert len(response.json["transaction_ids"]) == 2

@responses.activate
def test_unexistent_api_method(client):
    api_client = BindAPIClient()
    response = api_client.call("wrong_method")
    assert response.status_code == 200
    assert response.json["code"] == "ERR404"
    assert response.json["message"] == "Method doesn't exists. Check your call."
