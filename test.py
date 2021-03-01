import pprint

from blockchain import Blockchain
from transaction import Transaction

pp = pprint.PrettyPrinter(indent=4)
blockchain = Blockchain()
transactions = []

while True:
	sender = input("Please type in Sender Name: ")
	receiver = input("Please type in Receiver Name: ")
	amount = input("Please give the amount the sender will send: ")
	transaction = Transaction(sender, receiver, amount)
	transactions.append(transaction)
	restart = input("Make another transaction? Please type Yes/No: ")
	print(restart)
	if restart == "Yes":
		print("continuing")
		pass
	elif restart == "No":
		print("exiting")
		break
	else:
		print("invalid command")
		break


for one_transaction in transactions:
	blockchain.unconfirmed_transactions.append(one_transaction)

blockchain.mine_pending_transactions("darko")

pp.pprint(blockchain.chain_JSON_encode())
print("Length: ", len(blockchain.chain))

for person in users:
	person_amount = blockchain.get_balance(person)
	print("Amount {person}: {person_amount}")
