import json

def save_data(chain, transactions):
    try:
        with open('blockchain.json', mode='w') as f:
            json_file = {
                "blockchain": chain,
                "transactions": transactions
            }
            f.write(json.dumps(json_file))
    except IOError:
        print('Objeto não salvo.')

def read_data():
    try:
        with open('blockchain.json', mode='r') as f:
            return json.loads(f.readline())
    except (ValueError, IOError):
        return False
