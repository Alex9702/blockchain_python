from src.utility.ret_dict import ReturnDict

class Transactions(ReturnDict):
    def __init__(self, sender, receiver, amount, signature):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.signature = signature
