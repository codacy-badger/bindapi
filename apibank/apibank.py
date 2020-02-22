import os
import time
import requests

from .helpers import multi_replace_regex
from .url_constants import APIBANK_LOGIN_URL, APIBANK_TX_QUERY_URL, APIBANK_TX_CREATE_URL, APIBANK_ACC_QUERY_URL, \
    APIBANK_DEBIN_CREATE_URL, APIBANK_DEBIN_QUERY_URL, APIBANK_DEBIN_SUBSCRIPTION_CREATE_URL, \
    APIBANK_DEBIN_SUBSCRIPTION_QUERY_URL


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

    def __init__(self, account_id=None):
        self.account_id = os.getenv('BINDAPI_DEFAULT_ACCOUNT', account_id)

    def build_token(self):
        if self.token is None or not self.token.is_valid():
            created_at = time.time()
            response = requests.post(APIBANK_LOGIN_URL, json={
                "username": os.getenv('BINDAPI_USERNAME', None),
                "password": os.getenv('BINDAPI_PASSWORD', None)
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
            # in case of some unhandled error which we want to parse... do it here.
            pass

        return response_data

    def get_transfers(self):
        self.build_token()

        return self.handle_response(
            requests.get(
                APIBANK_TX_QUERY_URL,
                headers=self.token.auth_header({"obp_status": "COMPLETED"})
            )
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
                APIBANK_TX_CREATE_URL,
                headers=self.token.auth_header(),
                json=payload
            )
        )

    def account_detail(self, account, account_type="cbu"):
        self.build_token()

        query_params = {
            ":account_type": account_type,
            ":account_nro": account
        }

        return self.handle_response(
            requests.get(
                multi_replace_regex(APIBANK_ACC_QUERY_URL, query_params),
                headers=self.token.auth_header()
            )
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
                APIBANK_DEBIN_CREATE_URL,
                headers=self.token.auth_header(),
                json=payload
            )
        )

    def get_debin(self, debin_id):
        self.build_token()

        return self.handle_response(
            requests.get(
                APIBANK_DEBIN_QUERY_URL.replace(":transaction_id", debin_id),
                headers=self.token.auth_header()
            )
        )

    def create_debin_subscription(self, account_type, account_nro, description, provision, provision_reference,
                                  currency="ARS", concept="VAR"):
        if account_type not in ["cbu", "alias"]:
            return {"code": "ER001", "message": "Invalid account_type. Check your request parameters."}

        payload = {
            "to": {"cbu": account_nro} if account_type == "cbu" else {"label": account_nro},
            "value": {
                "currency": currency
            },
            "description": description,
            "concept": concept,
            "provision": provision,
            "provision_reference": provision_reference,
            "active": "true"
        }
        self.build_token()

        return self.handle_response(
            requests.post(
                APIBANK_DEBIN_SUBSCRIPTION_CREATE_URL,
                headers=self.token.auth_header(),
                json=payload
            )
        )

    def get_debin_subscription(self, transaction_id):
        self.build_token()

        return self.handle_response(
            requests.get(
                APIBANK_DEBIN_SUBSCRIPTION_QUERY_URL.replace(":transaction_id", transaction_id),
                headers=self.token.auth_header()
            )
        )
