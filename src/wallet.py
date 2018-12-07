import binascii
import Crypto.Random
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
import json

class Wallet:
    def __init__(self):
        self.keys = {}
        # self.pk = None
        # self.pr = None

    def create_keys(self):
        pr = (RSA.generate(1024,Crypto.Random.new().read))
        pk = pr.publickey()
        self.keys['private'] = pr.exportKey().decode('utf8')
        self.keys['public'] = pk.exportKey().decode('utf8')
        # self.keys['private'] = pr.exportKey().decode('utf8') # [31:-29].replace('\n', '')
        # self.keys['public'] = pk.exportKey().decode('utf8') # [27:-25].replace('\n', '')
    
    def save_keys(self, owner):
          with open(f'{owner}_wallet.json', 'w') as f:
            f.write(json.dumps(self.keys))


    def read_keys(self, owner):
        with open(f'{owner}_wallet.json', 'r') as f:
            self.keys = json.loads(f.read())


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

#### TESTES

owner = 'Max'

w = Wallet()
# w.create_keys()
# w.save_keys(owner)
w.read_keys(owner)
# print(w.keys)
t = {
    'sender': w.keys['public'],
    'receiver': 'Max',
    'amount': 50,
    'signature': None
}
t['signature'] = w.sign_transaction(t['sender'], 'Max', 50)
print(t)
# print(t)
# print(w.sign_transaction(t['sender'], 'Max', 50))
print(w.verify_transaction(t))


