from collections import OrderedDict
from hash_util import hash_string_256, hash_block
import json

MINING_REWARD = 10
owner = 'Max'

class Blockchain:
    def __init__(self):
        self.chain = []
        self.open_transactions = []
        self.participants = set()
        self.load_data()
        

    def create_chain(self, previous_hash='', proof=100):
        block = {
            'index': len(self.chain) + 1,
            'previous_hash': previous_hash,
            'proof':proof,
            'transactions': self.open_transactions if len(self.open_transactions) > 0 else []
        }
        self.chain.append(block)
        return block

    def load_data(self):
        try:
            with open('blockchain.txt', mode='r') as f:
                file_content = f.readlines()
                temp_chain = json.loads(file_content[0][:-1])
                temp_open_transactions = json.loads(file_content[1])
        except IOError:
            self.create_chain() # genesis block
            self.open_transactions = []
        finally:
            ordered_dicts = [[OrderedDict(
                    [('sender', tx['sender']), ('recipient', tx['recipient']), ('amount', tx['amount'])]
                )
                for tx in block['transactions']]
                for block in temp_chain]
            for (index, l) in enumerate(ordered_dicts):
                temp_chain

            # for block in temp_chain:
            #     for tx in block['transactions']:
            #         print(OrderedDict(
            #                 [('sender', tx['sender']), ('recipient', tx['recipient']), ('amount', tx['amount'])]
            #             ))

    def save_data(self):
        if self.verify_chain():
            try:
                with open('blockchain.txt', mode='w') as f:
                    f.write(json.dumps(self.chain))
                    f.write('\n')
                    f.write(json.dumps(self.open_transactions))
            except IOError:
                print('Saving failed!')

    def add_transaction(self, recipient, sender=owner, amount=1.0):
        transaction = OrderedDict(
            [('sender', sender),('recipient', recipient),('amount', amount)]
        )
        if self.verify_transaction(transaction):
            self.open_transactions.append(transaction)
            self.participants.add(sender)
            self.participants.add(recipient)
            self.save_data()
            return True
        return False

    def valid_proof(self, transactions, last_hash, proof):
        guess = (str(transactions) + str(last_hash) + str(proof)).encode()
        guess_hash = hash_string_256(guess)
        return guess_hash[0:2] == '00'

    def proof_of_work(self):
        last_block = self.chain[-1]
        last_hash = hash_block(last_block)
        proof = 0
        while not self.valid_proof(self.open_transactions, last_hash, proof):
            proof += 1
        return proof

    def mine_block(self):
        last_block = self.chain[-1]
        hashed_block = hash_block(last_block)
        proof = self.proof_of_work()

        reward_transaction = OrderedDict(
            [('sender', 'MINING'), ('recipient', owner), ('amount', MINING_REWARD)]
        )      
        self.open_transactions.append(reward_transaction)
        self.create_chain(hashed_block, proof)
        self.open_transactions = []
        self.save_data()
        return True

    def verify_chain(self):
        for (index, block) in enumerate(self.chain):
            if index == 0:
                continue
            if block['previous_hash'] != hash_block(self.chain[index - 1]):
                return False
            if not self.valid_proof(block['transactions'][:-1], block['previous_hash'], block['proof']):
                print('Proof of work is invalid')
                return False
        return True

    def printing_blockchain_elements(self):
        for block in self.chain:
            print('Outputting Block:')
            print(block)
        print('-'*20)
    
    def get_balance(self, participant):
        tx_sender = [[tx['amount'] for tx in block['transactions'] if tx['sender'] == participant] for block in self.chain]
        open_tx_sender = [tx['amount'] for tx in self.open_transactions if tx['sender'] == participant]
        tx_sender.append(open_tx_sender)
        amount_sent = sum([sum(tx) for tx in tx_sender if len(tx) > 0])

        tx_recipient = [[tx['amount'] for tx in block['transactions'] if tx['recipient'] == participant] for block in self.chain]
        amount_received = sum([sum(tx) for tx in tx_recipient if len(tx) > 0])

        return  amount_received - amount_sent

    def verify_transaction(self, transaction):
        sender_balance = self.get_balance(transaction['sender'])
        return sender_balance >= transaction['amount']

    def verify_transactions(self):
        return all([self.verify_transaction(tx) for tx in self.open_transactions])
