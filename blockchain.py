import json
from time import time
from utility.hash_util import hash_block
from utility.verification import Verification

MINING_REWARD = 10

class Blockchain:
    def __init__(self, hosting_node_id):
        self.hosting_node_id = hosting_node_id
        self.chain = []
        self.__open_transactions = []
        self.participants = set()
        # self.create_chain() # genesis block
        self.load_data()

    @property
    def chain(self):
        return self.__chain[:]

    @chain.setter
    def chain(self, val):
        self.__chain = val

    def create_chain(self, previous_hash='', proof=100):
        block = {
            'index':len(self.__chain),
            'previous_hash':previous_hash,
            'timestamp':time(),
            'transactions':self.__open_transactions,
            'proof':proof
        }
        self.__chain.append(block)
        return block

    def load_data(self):
        try:
            with open('blockchain.json', mode='r') as f:
                file_content = json.loads(f.read())
                self.chain = file_content[0]
                self.__open_transactions = file_content[1]

            self.get_participants()
        except IOError:
            self.create_chain() # genesis block
            self.__open_transactions = []
        finally:
            print('Cleanup!')
            Verification.verify_chain(self.__chain)


    def save_data(self):
        print(type(self.__chain))
        if Verification.verify_chain(self.__chain):
            try:
                with open('blockchain.json', mode='w') as f:
                    f.write(json.dumps([self.__chain, self.__open_transactions]))
            except IOError:
                print('Saving failed!')
 
    def get_participants(self):
        for block in self.chain:
            for participant in block['transactions']:
                if participant['sender'] != 'MINING':
                    self.participants.add(participant['sender'])
                if participant['recipient'] != 'MINING':
                    self.participants.add(participant['recipient'])
        
        for open_transaction in self.__open_transactions:
            self.participants.add(open_transaction['sender'])
            self.participants.add(open_transaction['recipient'])

    def add_transaction(self, recipient, sender, amount=1.0):
        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        }
        if Verification.verify_transaction(transaction, self.get_balance):
            self.__open_transactions.append(transaction)
            self.participants.add(sender)
            self.participants.add(recipient)
            self.save_data()
            return transaction
        return []

    def proof_of_work(self):
        last_block = self.__chain[-1]
        last_hash = hash_block(last_block)
        proof = 0
        while not Verification.valid_proof(self.__open_transactions, last_hash, proof):
            proof += 1
        return proof

    def mine_block(self):
        last_block = self.__chain[-1]
        hashed_block = hash_block(last_block)
        proof = self.proof_of_work()
        reward_transaction = {
            'sender': 'MINING', 
            'recipient': self.hosting_node_id, 
            'amount': MINING_REWARD
        }
        self.__open_transactions.append(reward_transaction)
        self.create_chain(hashed_block, proof)
        self.__open_transactions = []
        self.save_data()
        return True

    def printing_blockchain_elements(self):
        for block in self.__chain:
            print('Outputting Block:')
            print(block)
        print('-'*20)
    
    def get_balance(self):
        participant = self.hosting_node_id
        tx_sender = [[tx['amount'] for tx in block['transactions'] if tx['sender'] == participant] for block in self.__chain]
        open_tx_sender = [tx['amount'] for tx in self.__open_transactions if tx['sender'] == participant]
        tx_sender.append(open_tx_sender)
        amount_sent = sum([sum(tx) for tx in tx_sender if len(tx) > 0])

        tx_recipient = [[tx['amount'] for tx in block['transactions'] if tx['recipient'] == participant] for block in self.__chain]
        amount_received = sum([sum(tx) for tx in tx_recipient if len(tx) > 0])

        return  amount_received - amount_sent

    def get_open_transactions(self):
        return self.__open_transactions[:]


