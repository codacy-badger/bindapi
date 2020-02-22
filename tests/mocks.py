# All the following mocks were taken from the official apibank examples responses

APIBANK_TX_QUERY_MOCK = [
 {
   "id": "1-30714423033-015315163611093-0",
   "type": "TRANSFER",
   "from": {
       "bank_id": "322",
       "account_id": "21-1-99999-4-6"
   },
  "counterparty": {
      "id": "30615423323",
      "name": "UNAVAILABLE",
      "id_type": "CUIT_CUIL",
      "bank_routing": {
          "scheme": "UNAVAILABLE",
          "address": None
      },
      "account_routing": {
          "scheme": "LABEL",
          "address": "AliasPrueba1234"
      }
  },
   "details": {
         "origin_id": "55789",
   },
   "transaction_ids": [
       "7-30779999580-000000000660389-1"
   ],
   "status": "COMPLETED",
   "start_date": "2018-04-12T18:53:29.269Z",
   "end_date": "2018-04-12T18:53:29.269Z",
   "challenge": None,
   "charge": {
       "summary": "COMPLETE_TRANS",
       "value": {
           "currency": "ARS",
           "amount": 10
       }
   }
 }
]

APIBANK_TX_CREATE_MOCK = {
  "id": "7-30779999580-000000000660389-1",
  "type": "TRANSFER",
  "from": {
      "bank_id": "322",
      "account_id": "21-1-99999-4-6"
  },
  "counterparty": {
      "id": "30615423323",
      "name": "UNAVAILABLE",
      "id_type": "CUIT_CUIL",
      "bank_routing": {
          "scheme": "UNAVAILABLE",
          "address": None
      },
      "account_routing": {
          "scheme": "LABEL",
          "address": "AliasPrueba1234"
      }
  },
  "details": {
         "origin_id": "55789",
  },
  "transaction_ids": [
      "7-30779999580-000000000660389-1"
  ],
  "status": "COMPLETED",
  "start_date": "2018-04-12T18:53:29.269Z",
  "end_date": "2018-04-12T18:53:29.269Z",
  "challenge": None,
  "charge": {
      "summary": "COMPLETE_TRANS",
      "value": {
          "currency": "ARS",
          "amount": 10
      }
  }
}

APIBANK_ACC_QUERY_MOCK = {
    "owners": [
        {
            "id": "20203385072",
            "display_name": "Parker, Peter",
            "id_type": "CUIT",
            "is_physical_person": True
        }
    ],
    "type": "CC",
    "is_active": True,
    "currency": "ARS",
    "label": "dsadsa",
    "account_routing": {
        "scheme": "CBU",
        "address": "3220001823001077580012"
    },
    "bank_routing": {
        "scheme": "NAME",
        "address": "BANCO INDUSTRIAL S.A.",
        "code": "322"
    }
}

APIBANK_DEBIN_MOCK = {
    "id": "JMRD06ZO9WX5Z125GP7XY3",
    "type": "DEBIN",
    "from": {
        "bank_id": "322",
        "account_id": "21-1-99999-4-6"
    },
    "details": {
        "origin_id": "556677",
        "buyer": {
            "cuit": "20312528046",
            "alias": "aliasCBU",
            "cbu": None,
            "name": "Alejandro M.",
            "bank_code": "322",
            "bank_description": "BANCO INDUSTRIAL S.A."
        }
    },
    "transaction_ids": [
        "7-30714423033-000000000123667-1"
    ],
    "status": "PENDING",
    "status_description": "AWAITING_CUSTOMER_CONFIRMATION",
    "start_date": "2018-04-12T18:53:29.269Z",
    "end_date": "2018-04-12T18:53:29.269Z",
    "challenge": None,
    "charge": {
        "summary": "VAR",
        "value": {
            "currency": "ARS",
            "amount": 10
        }
    }
}

APIBANK_DEBIN_SUBSCRIPTION_MOCK = {
    "id": "1511443312312321321213092984",
    "type": "DEBIN_SUBSCRIPTION",
    "details": {
        "origin_id": "556677",
        "concept": "EXP",
        "description": "A description for this subscription",
        "provision": "Prestacion 1",
        "provision_reference" : "Numero de documento",
        "buyer": {
            "alias": "aliasCBU",
        }
    },
    "transaction_ids": [
        "15114433092984",
        "0"
    ],
    "status": "ACTIVE",
    "start_date": "2018-04-12T18:53:29.269Z",
    "end_date": "2018-04-12T18:53:29.269Z",
    "challenge": None,
    "charge": {
        "summary": "COMPLETE",
        "value": {
            "currency": "ARS"
        }
    }
}