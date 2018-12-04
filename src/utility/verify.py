from src.utility.hash_util import hash_block, hash_sha_256

class Verify:
    def is_chain_valid(self, chain):
        for (index, block) in enumerate(chain):
            if index == 0:
                continue
            if block['previous_hash'] != hash_block(chain[index - 1]):
                return False
            if not self.verify_proof(block['proof'], chain[index-1]['proof']):
                return False
        return True
    @staticmethod
    def verify_proof(proof, previous_proof):
        return hash_sha_256(str(proof**2 - previous_proof**2))[0:4] == '0000'