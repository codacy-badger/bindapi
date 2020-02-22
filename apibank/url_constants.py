import os


bank_id = os.getenv('BINDAPI_DEFAULT_BANKID', None)
account_id = os.getenv('BINDAPI_DEFAULT_ACCOUNT', None)

APIBANK_BASE_URL = "https://sandbox.bind.com.ar/v1"

APIBANK_LOGIN_URL = "{0}/login/jwt".format(APIBANK_BASE_URL)

# see https://sandbox.bind.com.ar/apidoc/
APIBANK_SELF_ACC_URL = "{0}/banks/{1}/accounts/{2}/owner".format(APIBANK_BASE_URL, bank_id, account_id)
APIBANK_TX_QUERY_URL = "{0}/transaction-request-types/TRANSFER".format(APIBANK_SELF_ACC_URL)
APIBANK_TX_CREATE_URL = "{0}/transaction-requests".format(APIBANK_TX_QUERY_URL)
APIBANK_ACC_QUERY_URL = "{0}/accounts/:account_type/:account_nro".format(APIBANK_BASE_URL)
APIBANK_DEBIN_CREATE_URL = "{0}/transaction-request-types/{1}/transaction-requests".format(
    APIBANK_SELF_ACC_URL, "DEBIN"
)
APIBANK_DEBIN_QUERY_URL = "{0}/transaction-request-types/{1}/:transaction_id".format(APIBANK_SELF_ACC_URL, "DEBIN")
APIBANK_DEBIN_SUBSCRIPTION_CREATE_URL = "{0}/banks/322/owner/transaction-request-types/{1}/transaction-requests".format(
    APIBANK_BASE_URL, "DEBIN-SUBSCRIPTION"
)
APIBANK_DEBIN_SUBSCRIPTION_QUERY_URL = "{0}/transaction-request-types/{1}/:transaction_id".format(
    APIBANK_SELF_ACC_URL, "DEBIN-SUBSCRIPTION"
)
