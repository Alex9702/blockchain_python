from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
import Crypto.Random
import binascii

class Wallet:
    def __init__(self):
        self.pk = None
        self.pr = None

    def create_keys(self):
        pr = RSA.generate(1024,Crypto.Random.new().read)
        pk = pr.publickey()
        self.pr = pr.exportKey()
        self.pk = pk.exportKey()
    
    def save_keys(self):
        with open('private.pem', mode='wb') as f:
            f.write(self.pr)
        with open('public.pem', mode='wb') as f:
            f.write(self.pk)
        
    def read_keys(self):
        with open('private.pem', mode='rb') as f:
            self.pr = f.read()
        with open('public.pem', mode='rb') as f:
            self.pk = f.read()
    
    def sign_transaction(self, sender, receiver, amount):
        key = RSA.importKey(self.pr)
        h = SHA256.new((str(sender) + str(receiver) + str(amount)).encode())
        signer = PKCS1_v1_5.new(key)
        signature = signer.sign(h)
        return signature

    @staticmethod
    def veriify_transaction(transaction):
        pk = RSA.importKey(transaction['sender'])
        h = SHA256.new((str(transaction['sender']) + str(transaction['receiver']) + str(transaction['amount'])).encode())
        verifier = PKCS1_v1_5.new(pk)
        return verifier.verify(h, transaction['signature'])

w = Wallet()
w.read_keys()

transaction = {
    'sender':'Alex',
    'receiver': 'Max',
    'amount': 50,
    'signature': None
}

transaction['sender'] = w.pk
transaction['signature'] = w.sign_transaction(transaction['sender'], transaction['receiver'], transaction['amount'])

print(Wallet.veriify_transaction(transaction))
