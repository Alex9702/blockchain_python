from flask import Flask, jsonify, request
from flask_restful import reqparse, abort, Api, Resource
from src.blockchain import Blockchain

app = Flask(__name__)
api = Api(app)

blockchain = Blockchain('Alex')

class Get_Chain(Resource):
    def get(self):
        response = {'chain': blockchain.chain,
                    'length': len(blockchain.chain)}

        return response, 200

class Add_Transaction(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('sender', required=True, help='Obrigatório!')
        parser.add_argument('receiver', required=True, help='Obrigatório!')
        parser.add_argument('amount', type=float, required=True, help='Obrigatório!')
        args = parser.parse_args()
        index = blockchain.add_transaction(args['sender'], args['receiver'], args['amount'])
        response = {'mensagem': f'Esta transação será adicionada ao bloco {index}'}
        return response, 201

class Mine_Block(Resource):
    def get(self):
        if blockchain.mine_block('Alex'):
            block = blockchain.last_block()
            response = {'Mensagem': 'Parabéns, bloco minerado!',
                        'index': block['index'],
                        'timestamp': block['timestamp'],
                        'proof': block['proof'],
                        'previous_hash': block['previous_hash'],
                        'transactions': block['transactions']
                    }
        else:
            response = {'mensagem':f'{blockchain.hosting_node}, você não tem importância suficiente para esta transação!'}
        return response

class Is_Valid(Resource):
    def get(self):
        is_valid = blockchain.is_valid_chain()
        if is_valid:
            response = {'mensagem': 'Tudo bem. O Blockchain é válido.'}
        else:
            response = {'mensagem': 'Erro: Blockchain inválido.'}
        return response


##
## Actually setup the Api resource routing here
##
api.add_resource(Get_Chain, '/get_chain')
api.add_resource(Add_Transaction, '/add_transaction')
api.add_resource(Mine_Block, '/mine_block')
api.add_resource(Is_Valid, '/is_valid')


if __name__ == '__main__':
    app.run(debug=True)