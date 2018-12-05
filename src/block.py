from time import time

class Block:
    def __init__(self, index, proof, previous_hash, transactions, timestamp=time()):
        self.index = index
        self.timestamp = timestamp
        self.proof = proof
        self.previous_hash = previous_hash
        self.transactions = transactions
    
    def __repr__(self):
        return str(self.__dict__)
 