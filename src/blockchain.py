from src.utility.hash_util import hash_block, hash_sha_256
from src.utility.verify import Verify
from src.block import Block
from src.transaction import Transation

MINING_REWARD = 10

class Blockchain:
    def __init__(self):
        self.hosting_node = 'Alex'
        self.chain = []
        self.transactions = []
        self.create_block() # criando genesis block
    
    def create_block(self, previous_hash='', proof=1):
        block = Block(len(self.chain) + 1, proof, previous_hash, self.transactions.copy())
        self.chain.append(block)
        return block

    def get_balance(self):
        pass
    
    def get_blockchain(self):
        blockchain = [block.__dict__ for block in self.chain]
        for (index, block) in enumerate(self.chain):
            blockchain[index]['transactions'] = [transaction.__dict__ for transaction in block.transactions]
        return blockchain

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
        transaction = Transation(sender, receiver, amount)
        self.transactions.append(transaction)
        return self.last_block().index + 1
    
    def mine_block(self, miner):
        previous_block = self.last_block()
        hashed_block = hash_block(previous_block)
        proof = self.proof_of_work(previous_block.proof)
        reward_transaction = Transation('MINING', miner, MINING_REWARD)
        self.transactions.append(reward_transaction)
        self.create_block(hashed_block, proof)
        self.transactions = []
        return self.last_block()
    
    def is_valid_chain(self):
        verify = Verify()
        return verify.is_chain_valid(self.chain)
