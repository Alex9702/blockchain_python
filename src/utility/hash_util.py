import hashlib
import json

def hash_sha_256(string):
     return hashlib.sha256(string.encode()).hexdigest()

def hash_block(block):
     new_block = block.get_dict()
     new_block['transactions'] = [transaction.get_dict() for transaction in block.transactions]
     return hash_sha_256(json.dumps(new_block, sort_keys=True))
