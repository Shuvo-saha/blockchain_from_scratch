import hashlib
import json
from datetime import datetime

from Crypto.Signature import *


class Transaction:
	def __init__(self, sender, receiver, amount):
		self.sender = sender
		self.receiver = receiver
		self.amount = amount
		self.time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
		self.hash = self.calculate_hash()
		self.signature = ""

	def calculate_hash(self):
		hash_string = self.sender + self.receiver + str(self.amount) + str(self.time)
		block_string = json.dumps(hash_string, sort_keys=True)
		return hashlib.sha256(block_string.encode()).hexdigest()

	def is_valid_transaction(self):

		if self.hash != self.calculate_hash():
			return False
		if self.sender == self.receiver:
			return False
		if self.sender == "Miner Rewards":
			return True
		if not self.signature or len(self.signature) == 0:
			print("no signature!")
			return False
		return True

	def sign_transaction(self, key, sender_key):
		if self.hash != self.calculate_hash():
			print("transaction tampered error")
			return False
		if str(key.publickey().export_key()) != str(sender_key.publickey().export_key()):
			print("Transaction attempt to be signed from another wallet")
			return False

		self.signature = "made"
		print("made signature!")
		return True
