APIBANK_BASE_URL = "https://sandbox.bind.com.ar/v1"

APIBANK_LOGIN_URL = "{0}/login/jwt".format(APIBANK_BASE_URL)

# see https://sandbox.bind.com.ar/apidoc/
APIBANK_SELF_ACC_URL = "{0}/banks/322/accounts/:account_id/owner".format(APIBANK_BASE_URL)
APIBANK_TX_QUERY_URL = "{0}/transaction-request-types/TRANSFER".format(APIBANK_SELF_ACC_URL)
APIBANK_TX_CREATE_URL = "{0}/transaction-requests".format(APIBANK_TX_QUERY_URL)
APIBANK_ACC_QUERY_URL = "{0}/accounts/:account_type/:account_nro".format(APIBANK_BASE_URL)
APIBANK_DEBIN_CREATE_URL = "{0}/transaction-request-types/DEBIN/transaction-requests".format(APIBANK_SELF_ACC_URL)
APIBANK_DEBIN_QUERY_URL = "{0}/transaction-request-types/DEBIN/:transaction_id".format(APIBANK_SELF_ACC_URL)
