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
        self.pr, self.pk = self.generate_keys()

    def generate_keys(self):
        pr = RSA.generate(1024, Crypto.Random.new().read)
        pk = pr.publickey()
        return (binascii.hexlify(pr.export_key(format='DER')).decode('ascii'), binascii.hexlify(pk.export_key(format='DER')).decode('ascii'))

    def save_keys(self):
        if self.pr != None and self.pk != None:
            try:
                with open('private.pem', mode='w') as f:
                    f.write(self.pr)
                with open('public.pem', mode='w') as f:
                    f.write(self.pk)
            except (IOError, IndexError):
                print('Saving keys failed!')

    
    def load_keys(self):
        try:
            with open('private.pem', mode='r') as f:
                self.pr = f.readline()
            with open('public.pem', mode='r') as f:
                self.pk = f.readline()
        except (IOError, IndexError):
            print('Saving keys failed!')
    
    def sign_transaction(self, sender, receiver, amount):
        signer = PKCS1_v1_5.new(RSA.import_key(binascii.unhexlify(self.pr)))
        h = SHA256.new((str(sender) + str(receiver) + str(amount)).encode('utf8'))
        signature = signer.sign(h)
        return binascii.hexlify(signature).decode('ascii')

    @staticmethod
    def verify_transaction(transaction):
        pk = RSA.binascii.unhexlify(transaction['sender'])
        verifier = PKCS1_v1_5.new(pk)
        h = SHA256.new((str(transaction['sender']) + str(transaction['receiver']) + str(transaction['amount'])).encode('utf8'))
        return verifier.verify(h, binascii.unhexlify(transaction['signature']))
        # verifier = PKCS1_v1_5.new(pk)
        # return verifier.verify(h, binascii.unhexlify(transaction['signature']))

w = Wallet()
w.load_keys()

# ('Alex', 'Max', 30)
transaction = {
    'sender':w.sign_transaction('Alex', 'Max', 50),
    'receiver':'Max',
    'amount': 50,
    'signature': ''
}

print(Wallet.verify_transaction(transaction))