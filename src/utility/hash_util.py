import hashlib
import json

def hash_sha_256(string):
     return hashlib.sha256(string.encode()).hexdigest()

def hash_block(block):
    return hash_sha_256(json.dumps(block, sort_keys=True))