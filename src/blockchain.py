import datetime
from src.utility.hash_util import hash_block, hash_sha_256
from src.utility.verify import Verify

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
            'transactions': self.transactions[:]
        }
        self.chain.append(block)
        return block
    
 
    def proof_of_work(self, previous_proof):
        proof = 1
        while True:
            hash_operation = hash_sha_256(str(proof**2 - previous_proof**2))
            if hash_operation[0:4] == '0000':
                return proof
            proof += 1

    def print_blockchain_value(self, blockchain):
        for block in blockchain:
            print(20 * '-', ' Outputting block ', 20 * '-')
            print(block)
        else:
            print(20 * '-')

    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({
            'sender':sender,
            'receiver':receiver,
            'amount':amount
        })
        return self.chain[-1]['index'] + 1

    
    def mine_block(self):
        previous_block = self.chain[-1]
        hashed_block = hash_block(previous_block)
        proof = self.proof_of_work(previous_block['proof'])
        self.create_block(hashed_block, proof)
        self.transactions = []
        return self.chain[-1]
    
    def is_valid_chain(self, chain):
        verify = Verify()
        return verify.is_chain_valid(chain)


    def __repr__(self):
        return str(self.chain)
