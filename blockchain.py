from datetime import datetime
from urllib.parse import urlparse

import requests
from Crypto.PublicKey import RSA

from block import Block
from transaction import Transaction


class Blockchain:
	def __init__(self):
		self.unconfirmed_transactions = []
		self.chain = [self.create_genesis_block()]
		self.difficulty = 2
		self.miner_rewards = 50
		self.block_size = 10
		self.nodes = set()

	def register_node(self, address):
		parsed_url = urlparse(address)
		self.nodes.add(parsed_url.netloc)

	def resolve_conflicts(self):
		neighbors = self.nodes
		new_chain = None
		max_length = len(self.chain)

		for node in neighbors:
			response = requests.get(f'http://{node}/chain')
			if response.status_code == 200:
				length = response.json()["length"]
				chain = response.json()["chain"]

				if length > max_length and self.is_valid_chain():
					max_length = length
					new_chain = chain

		if new_chain:
			self.chain = self.chain_JSON_decode(new_chain)
			print(self.chain)
			return True

		return False

	def mine_pending_transactions(self, miner):
		len_pt = len(self.unconfirmed_transactions)
		if len_pt <= 1:
			print("Not enough transactions to mine! Must be >1")
			return False
		else:
			for i in range(0, len_pt, self.block_size):
				end = i + self.block_size
				if i >= len_pt:
					end = len_pt
				transaction_slice = self.unconfirmed_transactions[i:end]
				new_block = Block(transaction_slice, datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), len(self.chain))
				hash_val = self.get_last_block().hash
				new_block.prev = hash_val
				new_block.mine_block(self.difficulty)
				self.chain.append(new_block)
			print("Mining transaction success")

			pay_miner = Transaction("Miner Rewards", miner, self.miner_rewards)
			self.unconfirmed_transactions = [pay_miner]
		return True

	def add_transaction(self, sender, receiver, amount, key_string, sender_key):
		key_byte = key_string.encode("ASCII")
		sender_key_byte = sender_key.encode("ASCII")

		key = RSA.import_key(key_byte)
		sender_key = RSA.import_key(sender_key_byte)

		if not sender or not receiver or not amount:
			print("transaction error: info missing")
			return False
		transaction = Transaction(sender, receiver, amount)
		transaction.sign_transaction(key, sender_key)
		if not transaction.is_valid_transaction():
			print("transaction error: transaction invalid")
		self.unconfirmed_transactions.append(transaction)
		return len(self.chain) + 1

	def get_last_block(self):
		return self.chain[-1]

	@staticmethod
	def create_genesis_block():
		arr = [Transaction("me", "you", 10)]
		genesis_block = Block(arr, datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), 0)
		genesis_block.prev = "None"
		return genesis_block

	def is_valid_chain(self):
		for i in range(1, len(self.chain)):
			block_1 = self.chain[i - 1]
			block_2 = self.chain[i]
			if not block_2.has_valid_transactions():
				print("No valid transactions in current block")
				return False
			if block_2.hash != block_2.compute_hash():
				print("Hash doesn't match")
				return False
			if block_2.prev != block_1.hash:
				print("Previous hash doesn't match")
				return False
		return True

	@staticmethod
	def generate_keys():
		key = RSA.generate(2048)
		private_key = key.export_key()
		file_out = open("private.pem", "wb")
		file_out.write(private_key)

		public_key = key.publickey().export_key()
		file_out = open("receiver.pem", "wb")
		file_out.write(public_key)
		print(public_key.decode("ASCII"))
		return key.publickey().export_key().decode("ASCII")

	def chain_JSON_encode(self):
		block_arr_JSON = []
		for block in self.chain:
			block_JSON = {"hash": block.hash, "index": block.index, "prev": block.prev, "time": block.timex,
			              "nonce": block.nonce, "gym": block.gym}

			transactions_JSON = []
			t_JSON = {}
			for transaction in block.transactions:
				t_JSON["time"] = transaction.time
				t_JSON["sender"] = transaction.sender
				t_JSON["receiver"] = transaction.receiver
				t_JSON["amount"] = transaction.amount
				t_JSON["hash"] = transaction.hash
				transactions_JSON.append(t_JSON)

			block_JSON["transactions"] = transactions_JSON
			block_arr_JSON.append(block_JSON)
		return block_arr_JSON

	@staticmethod
	def chain_JSON_decode(chain_JSON):
		chain = []
		for block_JSON in chain_JSON:
			arr = []
			for t_JSON in block_JSON["transactions"]:
				transaction = Transaction(t_JSON["sender"], t_JSON["receiver"], t_JSON["amount"])
				transaction.time = t_JSON["time"]
				transaction.hash = t_JSON["hash"]
				arr.append(transaction)

			block = Block(arr, block_JSON["time"], block_JSON["index"], block_JSON['prev'])
			block.hash = block_JSON["hash"]
			block.prev = block_JSON["prev"]
			block.nonce = block_JSON["nonce"]
			block.gym = block_JSON["gym"]

			chain.append(block)

		return chain

	def get_balance(self, person):
		balance = 0
		for i in range(1, len(self.chain)):
			block = self.chain[i]
			try:
				for j in range(0, len(block.transactions)):
					transaction = block.transactions[j]
					if transaction.sender == person:
						balance -= transaction.amount
					if transaction.receiver == person:
						balance += transaction.amount
			except AttributeError:
				print("no transaction")
		return balance + 100
