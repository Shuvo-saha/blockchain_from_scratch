import pprint

from blockchain import Blockchain
from transaction import Transaction

pp = pprint.PrettyPrinter(indent=4)
blockchain = Blockchain()

input("Please type in Sender Name: ")
input("Please type in Receiver Name: ")
transaction = Transaction("Dan Rogers", "Shuvo", 155)
transaction2 = Transaction("Shuvo", "Dan Rogers", 10)
transaction3 = Transaction("Shuvo", "Martin", 10)

blockchain.unconfirmed_transactions.append(transaction) for transaction in transactions

blockchain.mine_pending_transactions("darko")

pp.pprint(blockchain.chain_JSON_encode())
print("Length: ", len(blockchain.chain))
print("Balance Shuvo: ", blockchain.get_balance("Shuvo"))
print("Balance Dan Rogers: ", blockchain.get_balance("Dan Rogers"))
print("Balance Martin: ", blockchain.get_balance("Martin"))
