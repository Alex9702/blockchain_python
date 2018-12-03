from blockchain import Blockchain
from utility.verification import Verification



class Node:
    def __init__(self):
        self.id = 'Max'
        self.blockchain = Blockchain(self.id)

    def get_user_choice(self):
        user_input = input('Your choice:')
        return user_input

    def get_transaction_value(self):
        tx_recipient = input('Enter the recipient of the transaction:')
        tx_amount = float(input('Your transaction amount please:'))
        return tx_recipient, tx_amount

    def wait_input(self):
        
        waiting_for_input = True

        while waiting_for_input:
            print('\n')
            print('Please choose')
            print('1: Add a new transaction value')
            print('2: Mine a new block')
            print('3: Output the blockchain blocks')
            print('4: Output participants')
            print('5: Check transaction validity')
            print('q: Quit')
            user_choice = self.get_user_choice()

            if user_choice == '1':
                tx_data = self.get_transaction_value()
                recipient, amount = tx_data
                if self.blockchain.add_transaction(recipient, self.id, amount):
                    print('Added transaction!')
                else:
                    print('Transaction failed!')

            elif user_choice == '2':
                self.blockchain.mine_block()
            elif user_choice == '3':
                self.blockchain.printing_blockchain_elements()
            elif user_choice == '4':
                print(self.blockchain.participants)
            elif user_choice == '5':
                if Verification.verify_transactions(self.blockchain.get_open_transactions(), self.blockchain.get_balance):
                    print('All transactions are valid')
                else:
                    print('There are invalid transactions')
            elif user_choice == 'q':
                waiting_for_input = False
            else:
                print('Input was invalid, please pick a value from the list!')

            if not Verification.verify_chain(self.blockchain.chain):
                self.blockchain.printing_blockchain_elements()
                print('Invalid blockchain!')
                break
            print('Balance of {}: {:6.2f}'.format('Max', self.blockchain.get_balance()))
        else:
            print('User left!')
        print('Done!')

if __name__ == '__main__':
    node = Node()
    node.wait_input()