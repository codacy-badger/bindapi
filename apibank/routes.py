import apibank
from apibank.apibank import BindAPIClient
from flask import jsonify, request

api_client = BindAPIClient()


def configure_routes(app):
    @app.route('/')
    def hello():
        return "Hello World!"

    @app.route('/count')
    def count():
        apibank.redisClient.incr('hits')
        return "{0} Hello World!".format(apibank.redisClient.get('hits'))

    @app.route('/transfers', methods=['GET'])
    def get_transfers():
        return jsonify(api_client.call("get_transfers"))

    @app.route('/transfer', methods=['POST'])
    def make_transfer():
        return jsonify(api_client.call("create_transfer", **request.json))

    @app.route('/account_details', methods=['POST'])
    def account_detail():
        args = {
            "account_type": "cbu" if "cbu" in request.json.keys() else "alias",
        }
        args["account"] = request.json[args["account_type"]]

        return jsonify(api_client.call("account_detail", **args))

    @app.route('/debin', methods=['POST', 'GET'])
    def debin_handler():
        method = "create_debin" if request.method == 'POST' else "get_debin"
        return jsonify(api_client.call(method, **request.json))

    @app.route('/debin-subscription', methods=['POST', 'GET'])
    def debin_subscription_handler():
        method = "get_debin_subscription"
        if request.method == 'POST':
            if len({"account_type",
                    "account_nro",
                    "description",
                    "provision",
                    "provision_reference"}.intersection(request.json)) != 5:
                return {"code": "ER001", "message": "Missing mandatory parameters. Check your request parameters."}
            method = "create_debin_subscription"
        return jsonify(api_client.call(method, **request.json))
