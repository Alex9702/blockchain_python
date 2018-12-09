from time import time
from src.utility.ret_dict import ReturnDict
class Block(ReturnDict):
    def __init__(self, index, previous_hash, proof, transactions, timestamp=time()):
        self.index = index
        self.previous_hash = previous_hash
        self.proof = proof
        self.transactions = transactions
        self.timestamp = timestamp
