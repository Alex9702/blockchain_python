from blockchain import Blockchain

b = Blockchain()

class Node:
    def __init__(self):
        self.waiting_for_input = True
    def get_user_choice(self):
        user_input = input('Your choice:')
        return user_input

    def get_transaction_value(self):
        tx_recipient = input('Enter the recipient of the transaction:')
        tx_amount = float(input('Your transaction amount please:'))
        return tx_recipient, tx_amount

    def verify_transactions(self):
        return all([b.verify_transaction(tx) for tx in b.open_transactions])

    def wait_input(self):

        while self.waiting_for_input:
            print('Please choose')
            print('1: Add a new transaction value')
            print('2: Mine a new block')
            print('3: Output the blockchain blocks')
            print('4: Output participants')
            print('5: Check transaction validity')
            print('h: Manipulate the chain')
            print('q: Quit')
            user_choice = self.get_user_choice()

            if user_choice == '1':
                tx_data = self.get_transaction_value()
                recipient, amount = tx_data
                if b.add_transaction(recipient, amount=amount):
                    print('Added transaction!')
                else:
                    print('Transaction failed!')

            elif user_choice == '2':
                b.mine_block()
            elif user_choice == '3':
                b.printing_blockchain_elements()
            elif user_choice == '4':
                print(b.participants)
            elif user_choice == '5':
                if b.verify_transactions():
                    print('All transactions are valid')
                else:
                    print('There are invalid transactions')
            elif user_choice == 'q':
                self.waiting_for_input = False
            else:
                print('Input was invalid, please pick a value from the list!')

            if not b.verify_chain():
                b.printing_blockchain_elements()
                print('Invalid blockchain!')
                break
            print('Balance of {}: {:6.2f}'.format('Max', b.get_balance('Max')))
        else:
            print('User left!')
        print('Done!')

if __name__ == '__main__':
    node = Node()
    node.wait_input()