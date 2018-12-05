
class Transation:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
    def __repr__(self):
        return str(self.__dict__)