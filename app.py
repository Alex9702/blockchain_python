from flask import Flask, jsonify, request
from src.blockchain import Blockchain
from src.wallet import Wallet

app = Flask(__name__)

blockchain = Blockchain('bank')

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    json = request.get_json()
    transaction_keys = ['sender', 'receiver', 'amount']
    if not all(key in json for key in transaction_keys):
        return 'Está faltando algum elemento.', 400
    index = blockchain.add_transaction(json['sender'], json['receiver'], json['amount'])
    response = {'mensagem': f'Esta transação será adicionada ao bloco {index}'}
    return jsonify(response), 201


@app.route('/mine_block', methods=['GET'])
def mine_block():
    
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
            
    return jsonify(response), 200


@app.route('/get_chain', methods=['GET'])
def get_chain():
    
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200


@app.route('/is_valid', methods=['GET'])
def is_valid():
    is_valid = blockchain.is_valid_chain()
    if is_valid:
        response = {'mensagem': 'Tudo bem. O Blockchain é válido.'}
    else:
        response = {'mensagem': 'Erro: Blockchain inválido.'}
    return jsonify(response), 200

@app.route('/create_wallet', methods=['POST'])
def create_wallet():
    response_cod = None
    json = request.get_json()
    if json['wallet_id'] != '':
        w = Wallet()
        w.create_wallet(json['wallet_id'])
        if w.read_wallet(json['wallet_id']):
            response = {'mensagem':'Carteira já existe!', 'carteira':w.public}
        response =  {'mensagem':f'wallet({json["wallet_id"]}) -> {w.public}'}
    else:
        response =  {'mensagem':'Falta wallet_id!'}
        response_cod =  400
    return jsonify(response), response_cod if response_cod else 201

@app.route('/read_wallet')
@app.route('/read_wallet/')
@app.route('/read_wallet/<id>')
def read_wallet(id=None):
    w = Wallet()
    if id == None:
        response = {'mensagem':'Falda nome da wallet!'}
    elif w.read_wallet(id):
        response = {'nome':id,
                    'wallet':w.public}
    else:
        response = {'mensagem':f'Não existe cateira para: {id}, Favor criar!'}
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)