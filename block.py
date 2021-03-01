import hashlib
import json

import jsonpickle
from Crypto.Signature import *


# make a block class that contains the data of one block in the chain
class Block:
	def __init__(self, transactions, timex, index):
		self.index = index
		self.transactions = transactions
		self.timex = timex
		self.prev = ""
		self.nonce = 0
		self.gym = self.calculate_gym()
		self.hash = self.compute_hash()

	@staticmethod
	def calculate_gym():
		return "24 hr"

	def compute_hash(self):
		hash_transactions = ""
		for transaction in self.transactions:
			hash_transactions += transaction.hash
		hash_string = str(self.timex) + hash_transactions + self.prev + str(self.nonce)
		block_string = json.dumps(hash_string, sort_keys=True)
		return hashlib.sha256(block_string.encode()).hexdigest()

	def mine_block(self, difficulty):
		arr = []
		for i in range(0, difficulty):
			arr.append(i)

		arr_str = map(str, arr)
		hash_puzzle = "".join(arr_str)

		while self.hash[0:difficulty] != hash_puzzle:
			self.nonce += 1
			self.hash = self.compute_hash()

		print("Block Mined!")

		return True

	def has_valid_transactions(self):
		for i in range(0, len(self.transactions)):
			transaction = self.transactions[i]
			if not transaction.is_valid_transaction():
				return False
			return True

	def JSON_encode(self):
		return jsonpickle.encode(self)
