from datetime import datetime
from src.utility.hash_util import hash_block, hash_sha_256
from src.utility.verify import Verify
from src.db_json import save_data, read_data
from src.block import Block
from src.transactions import Transactions
from src.wallet import Wallet

MINING_REWARD = 10

class Blockchain:
    def __init__(self, hosting_node):
        self.wallet = Wallet()
        self.wallet.create_wallet(hosting_node)
        self.hosting_node = self.wallet.public
        self.chain = []
        self.transactions = []
        self.load_data()
    
    def create_block(self, previous_hash='', proof=100):
        block = Block(len(self.chain) + 1, previous_hash, proof, self.transactions[:]).get_dict()
        self.chain.append(block)
        return block

    def load_data(self):
        json_data = read_data()
        if json_data:
            self.chain = json_data['blockchain']
            self.transactions = json_data['transactions']
        else:
            self.save_data()

    def save_data(self):
        if len(self.chain) == 0:
            self.create_block()
        save_data(self.chain, self.transactions)
        self.load_data()

    def get_balance(self):
        participant = self.hosting_node

        tx_receiver = sum([tx['amount'] for block in self.chain for tx in block['transactions'] if tx['receiver'] == participant])

        tx_sender = sum([tx['amount'] for block in self.chain for tx in block['transactions'] if tx['sender'] == participant] +  [tx['amount'] for tx in self.transactions if tx['sender'] == participant])

        return tx_receiver - tx_sender


    def proof_of_work(self, previous_proof):
        proof = 1
        while True:
            hash_operation = hash_sha_256(str(proof**2 - previous_proof**2))
            if hash_operation[0:4] == '0000':
                return proof
            proof += 1

    def print_blockchain_value(self):
        for block in self.chain:
            print(20 * '-', ' Outputting block ', 20 * '-')
            print(str(block))
        else:
            print(20 * '-')

    def last_block(self):
        return self.chain[-1]

    def add_transaction(self, sender, receiver, amount):
        sender_wallet = Wallet()
        if not sender_wallet.read_wallet(sender):
            return 0
        sender = sender_wallet.public

        receiver_wallet = Wallet()
        if not receiver_wallet.read_wallet(receiver):
            return 0
        
        receiver = receiver_wallet.public
        transaction = Transactions(sender, receiver, amount, None)
        transaction.signature = sender_wallet.sign_transaction(transaction.get_dict())
        self.transactions.append(transaction.get_dict())
        self.save_data()
        return self.last_block()['index'] + 1
    
    def mine_block(self, miner):
        miner_wallet = Wallet()
        if not miner_wallet.read_wallet(miner):
            return False
        reward_transaction = Transactions(self.hosting_node, miner_wallet.public, MINING_REWARD, None)
        reward_transaction.signature = miner_wallet.sign_transaction(reward_transaction.get_dict())
        self.transactions.append(reward_transaction.get_dict())
        
        previous_block = self.last_block()
        hashed_block = hash_block(previous_block)
        proof = self.proof_of_work(previous_block['proof'])
        print([Wallet.verify_transaction(t) for t in self.transactions])
        return
        if all([Wallet.verify_transaction(t) for t in self.transactions]):
            if self.get_balance() > 0:
                self.create_block(hashed_block, proof)
                self.transactions = []
                self.save_data()
                return True
        self.transactions = []
        self.save_data()
        return False
    
    def is_valid_chain(self):
        self.load_data()
        verify = Verify()
        return verify.is_chain_valid(self.chain)

