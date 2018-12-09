from datetime import datetime
from src.utility.hash_util import hash_block, hash_sha_256
from src.utility.verify import Verify
from src.db_json import save_data, read_data
from src.block import Block
from src.transactions import Transactions
# from src.wallet import Wallet

MINING_REWARD = 10

class Blockchain:
    def __init__(self, hosting_node):
        self.hosting_node = hosting_node
        self.chain = []
        self.transactions = []
        self.save_data()
        # self.load_data()
        # self.wallet = None
    
    def create_block(self, previous_hash='', proof=100):
        block = Block(len(self.chain) + 1, previous_hash, proof, self.transactions[:])
        self.chain.append(block)
        return block.get_dict()

    def load_data(self):
        json_data = read_data()
        if json_data:
            # transactions = [Transactions(t['sender'], t['receiver'], t['amount'], t['signature']) for t in json_data['transactions']]
            # chain = [Block(b['index'], b['previous_hash'], b['proof'],b['transaction'], b['timestamp']) for b in json_data['blockchain']]
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
        
        tx_sender = [tx_amount['amount'] for block in self.chain 
                    for tx_amount in block['transactions'] 
                    if tx_amount['sender'] == participant]

        tr_sender = [tx_amount['amount'] for tx_amount in self.transactions 
                    if tx_amount['sender'] == participant]

        tx_sender = sum(tx_sender + tr_sender)

        tx_receiver = [tx_amount['amount'] for block in self.chain 
                    for tx_amount in block['transactions'] 
                    if tx_amount['receiver'] == participant]

        tr_receiver = [tx_amount['amount'] for tx_amount in self.transactions 
                      if tx_amount['receiver'] == participant]

        tx_receiver = sum(tx_receiver + tr_receiver)

        return tx_sender < tx_receiver

 

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
        
        transaction = Transactions(sender, receiver,amount, None)
        self.transactions.append(transaction)
        # self.save_data()
        return self.last_block().index + 1
    
    def mine_block(self, miner):
        previous_block = self.last_block()
        hashed_block = hash_block(previous_block)
        proof = self.proof_of_work(previous_block.proof)
        reward_transaction = Transactions(self.hosting_node, miner, MINING_REWARD, None)
        self.transactions.append(reward_transaction)
        # if self.get_balance():
        self.create_block(hashed_block, proof)
        self.transactions = []
            # self.save_data()
        #     return True
        # self.transactions = []
        # self.save_data()
        return False
    
    def is_valid_chain(self):
        # self.load_data()
        verify = Verify()
        return verify.is_chain_valid(self.chain)
