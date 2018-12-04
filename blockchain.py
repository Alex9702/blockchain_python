import datetime
import hashlib
import json

class Blockchain:
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_block() # criando genesis block
        
    def create_block(self, previous_hash='', proof=1):
        block = {
            'index': len(self.chain),
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'previous_hash':previous_hash,
            'transactions': self.transactions
        }
        self.chain.append(block)
        return block
    
    def hash_block(self, block):
        return hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()
    
    def proof_of_work(self, previous_proof):
        proof = 1
        while True:
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[0:4] == '0000':
                return proof
            proof += 1

    def verify_proof(self, proof, previous_proof):
        return hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()[0:4] == '0000'
        
        
    def print_blockchain_value(self, blockchain):
        for block in blockchain:
            print('Outputting block')
            print(block)
        else:
            print(20 * '-')

    def is_chain_valid(self, chain):
        for (index, block) in enumerate(chain):
            if index == 0:
                continue
            if block['previous_hash'] != self.hash_block(chain[index - 1]):
                return False
            if not self.verify_proof(block['proof'], chain[index-1]['proof']):
                return False
        return True
    def __repr__(self):
        return str(self.chain)

b = Blockchain()
b.create_block(b.hash_block(b.chain[-1]), b.proof_of_work(b.chain[-1]['proof']))
b.create_block(b.hash_block(b.chain[-1]), b.proof_of_work(b.chain[-1]['proof']))
b.print_blockchain_value(b.chain)
print(b.is_chain_valid(b.chain))
