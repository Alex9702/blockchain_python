import binascii
import Crypto.Random
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
import json

class Wallet:
    def __init__(self):
        self.keys = {}

    def create_keys(self):
        pr = (RSA.generate(1024, Crypto.Random.new().read))
        pk = pr.publickey()
        self.keys['private'] = pr.exportKey().decode('utf8')
        self.keys['public'] = pk.exportKey().decode('utf8')
    
    def create_wallet(self, owner):
        if not self.read_wallet(owner):
            self.create_keys()
            with open(f'{owner}_wallet.json', 'w') as f:
                f.write(json.dumps(self.keys))
        

    def read_wallet(self, owner):
        try:
            with open(f'{owner}_wallet.json', 'r') as f:
                self.keys = json.loads(f.read())
        except FileNotFoundError:
            return False
        return True


    def sign_transaction(self, sender, receiver, amount):
        pr = RSA.importKey(self.keys['private'])
        h = SHA256.new((str(sender) + str(receiver) + str(amount)).encode())
        signer = PKCS1_v1_5.new(pr)
        signature = signer.sign(h)
        return binascii.hexlify(signature).decode('ascii')

    @staticmethod
    def verify_transaction(transaction):
        pk = RSA.importKey(bytes(transaction['sender'].encode()))
        h = SHA256.new((str(transaction['sender']) + str(transaction['receiver']) + str(transaction['amount'])).encode())
        verifier = PKCS1_v1_5.new(pk)
        return verifier.verify(h, binascii.unhexlify(transaction['signature']))
    
    # def __create_bank(self):
    #     self.read_wallet('bank')
    #     bank = {
    #         'sender':'bank',
    #         'receiver':self.keys['public'],
    #         'amount': 100000000,
    #         'signature':None
    #     }
    #     bank['signature'] = self.sign_transaction(bank['sender'], )
    #     try:
    #         with open('bank_acount.json', 'w'):
    #             f.write(json(bank))


#### TESTES
#### Creating a banking
w = Wallet()
# w.create_keys()
w.create_wallet("Neto")
# print(w.read_wallet("bank"))
# print(w.keys)
t = {
    'sender': w.keys['public'],
    'receiver': w.keys['public'],
    'amount': 10000000000,
    'signature': None
}
t['signature'] = w.sign_transaction(t['sender'], t['receiver'], t['amount'])
print(t)
print(w.verify_transaction(t))


