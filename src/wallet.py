import binascii
import Crypto.Random
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
import json
import os

class Wallet:
    def __init__(self):
        self.public = None
        self.private = None

    def __create_keys(self):
        pr = (RSA.generate(1024, Crypto.Random.new().read))
        pk = pr.publickey()
        self.private = binascii.hexlify(pr.exportKey(format='DER')).decode('ascii')
        self.public = binascii.hexlify(pk.exportKey(format='DER')).decode('ascii')
    
    def create_wallet(self, owner):
        if len(owner) < 64:
            owner = SHA256.new(owner.encode()).hexdigest()
        if not self.read_wallet(owner):
            self.__create_keys()
            with open('{}\wallets\{}.json'.format(os.path.abspath(os.path.dirname('wallet.py')), owner), 'w') as f:
                f.write(json.dumps({
                    'public': self.public,
                    'private': self.private
                }))
    
    def read_wallet(self, owner):
        if len(owner) < 64:
            owner = SHA256.new(owner.encode()).hexdigest()
        try:
            with open('{}\wallets\{}.json'.format(os.path.abspath(os.path.dirname('wallet.py')), owner), 'r') as f:
                file_read = json.loads(f.read())
                self.public = file_read['public']
                self.private = file_read['private']
        except FileNotFoundError:
            return False
        return True

    def delete_wallet(self, owner):
        if len(owner) < 64:
            owner = SHA256.new(owner.encode()).hexdigest()
        if self.read_wallet(owner):
            os.remove('{}\wallets\{}.json'.format(os.path.abspath(os.path.dirname('wallet.py')), owner))
            return True
        return False

    def sign_transaction(self, transaction):
        pr = RSA.importKey(binascii.unhexlify(self.private))
        h = SHA256.new((str(transaction['sender']) + str(transaction['receiver']) + str(transaction['amount'])).encode())
        signer = PKCS1_v1_5.new(pr)
        signature = signer.sign(h)
        return binascii.hexlify(signature).decode('ascii')

    @staticmethod
    def verify_transaction(transaction):
        pk = RSA.importKey(binascii.unhexlify(transaction['sender']))
        h = SHA256.new((str(transaction['sender']) + str(transaction['receiver']) + str(transaction['amount'])).encode())
        verifier = PKCS1_v1_5.new(pk)
        return verifier.verify(h, binascii.unhexlify(transaction['signature']))
