from apibank.apibank import BindAPIClient
from flask import jsonify, request

api_client = BindAPIClient()

def configure_routes(app):
    @app.route('/')
    def hello():
        return "Hello World!"

    @app.route('/transfers', methods=['GET'])
    def get_transfers():
        return jsonify(api_client.get_transfers())

    @app.route('/transfer', methods=['POST'])
    def make_transfer():
        return jsonify(api_client.create_transfer(
            cbu=request.json["cbu"],
            amount=request.json["amount"],
            currency=request.json["currency"])
        )

    @app.route('/account_details', methods=['POST'])
    def account_detail():
        account_type = "cbu" if "cbu" in request.json.keys() else "alias"
        account = request.json[account_type]
        return jsonify(api_client.account_detail(account=account, account_type=account_type))

    @app.route('/debin', methods=['POST', 'GET'])
    def debin_handler():
        if request.method == 'POST':
            response = api_client.create_debin(cbu=request.json["cbu"],
                                               amount=request.json["amount"],
                                               currency=request.json["currency"])
        else:
            response = api_client.get_debin(debin_id=request.json["id"])

        return jsonify(response)

