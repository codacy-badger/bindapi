import time
import requests

from .helpers import multi_replace_regex
from .url_constants import APIBANK_LOGIN_URL, APIBANK_TX_QUERY_URL, APIBANK_TX_CREATE_URL, APIBANK_ACC_QUERY_URL, \
    APIBANK_DEBIN_CREATE_URL, APIBANK_DEBIN_QUERY_URL


class BindToken:

    def __init__(self, data, created_at=None):
        self.expiration = data["expires_in"]
        self.token = data["token"]
        self.created_at = time.time() - 5 if created_at is None else created_at

    def is_valid(self):
        return time.time() < self.created_at + self.expiration

    def auth_header(self, custom_headers=None):
        if self.is_valid():
            auth_header = {'Authorization': 'JWT {0}'.format(self.token)}

            if custom_headers and type(custom_headers) is dict:
                auth_header = {**auth_header, **custom_headers}
            return auth_header
        raise Exception("Token expired: please renew it")


class BindAPIClient:
    token = None

    def __init__(self, account_id="21-1-99999-4-6"):
        self.account_id = account_id

    def build_token(self):
        if self.token is None or not self.token.is_valid():
            created_at = time.time()
            response = requests.post(APIBANK_LOGIN_URL, json={
                "username": "federico@xeta.com.ar",
                "password": "OgIGyehigOOGqSR"
            })
            if response.status_code == 200:
                self.token = BindToken(response.json(), created_at)
            else:
                response = response.json()
                raise Exception("{0}:{1}".format(response["code"], response["message"]))
        return self.token

    def handle_response(self, response, url_to_parse=None):
        response_data = response.json()

        if response.status_code != 200:
            raise Exception("Error code {0}: {1}".format(response_data["code"], response_data["message"]))
        else:
            if url_to_parse == APIBANK_TX_QUERY_URL:
                response_data = list(map(lambda tx: {
                    "id": tx["id"],
                    "cuil": tx["counterparty"]["id"],
                    "amount": tx["charge"]["value"]["amount"],
                    "currency": tx["charge"]["value"]["currency"]
                }, response_data))
            elif url_to_parse == APIBANK_TX_CREATE_URL:
                response_message = "Transferencia exitosa" if response_data["status"] == "COMPLETED" \
                    else "Transferencia rechazada"
                response_data = {"message": response_message}
            elif url_to_parse == APIBANK_ACC_QUERY_URL:
                response_data = {
                    "cbu": response_data["account_routing"]["address"],
                    "alias": "",
                    "currency": response_data["currency"],
                    "cuil": response_data["owners"][0]["id"],
                    "bank_name": response_data["bank_routing"]["address"],
                    "fullname": response_data["owners"][0]["display_name"],
                }
            elif url_to_parse == APIBANK_DEBIN_CREATE_URL:
                response_data = {
                    "id": response_data["id"],
                    "message": "Pedido de DEBIN creado" if response_data["status"] in ["PENDING"]
                                                        else "Pedido de DEBIN NO creado"
                }
            elif url_to_parse == APIBANK_DEBIN_QUERY_URL:
                response_data = {
                    "completed": True if response_data["status"] in ["COMPLETED", "ACREDITADO"] else False
                }
            else:
                response_data = {"message": "Invalid url"}
            return response_data

    def get_transfers(self):
        self.build_token()

        return self.handle_response(
            requests.get(
                APIBANK_TX_QUERY_URL.replace(":account_id", self.account_id),
                headers=self.token.auth_header({"obp_status": "COMPLETED"})
            ), url_to_parse=APIBANK_TX_QUERY_URL
        )

    def create_transfer(self, cbu, amount, currency="ARS"):
        self.build_token()

        payload = {
            "to": {
                "cbu": cbu
            },
            "value": {
                "currency": currency,
                "amount": amount
            },
            "concept": "VAR"
        }

        return self.handle_response(
            requests.post(
                APIBANK_TX_CREATE_URL.replace(":account_id", self.account_id),
                headers=self.token.auth_header(),
                json=payload
            ), url_to_parse=APIBANK_TX_CREATE_URL
        )

    def account_detail(self, account, account_type="cbu"):
        self.build_token()

        query_params = {
            ":account_type": account_type,
            ":account_nro": account
        }
        print(multi_replace_regex(APIBANK_ACC_QUERY_URL, query_params))
        return self.handle_response(
            requests.get(
                multi_replace_regex(APIBANK_ACC_QUERY_URL, query_params),
                headers=self.token.auth_header()
            ), url_to_parse=APIBANK_ACC_QUERY_URL
        )

    def create_debin(self, cbu, amount, currency="ARS"):
        self.build_token()

        payload = {
            "to": {
                "cbu": cbu
            },
            "value": {
                "currency": currency,
                "amount": amount
            },
            "concept": "VAR",
            "expiration": 4320  # max value
        }
        return self.handle_response(
            requests.post(
                APIBANK_DEBIN_CREATE_URL.replace(":account_id", self.account_id),
                headers=self.token.auth_header(),
                json=payload
            ), url_to_parse=APIBANK_DEBIN_CREATE_URL
        )

    def get_debin(self, debin_id):
        self.build_token()

        query_params = {
            ":account_id": self.account_id,
            ":transaction_id": debin_id
        }
        return self.handle_response(
            requests.get(
                multi_replace_regex(APIBANK_DEBIN_QUERY_URL, query_params),
                headers=self.token.auth_header()
            ), url_to_parse=APIBANK_DEBIN_QUERY_URL
        )
