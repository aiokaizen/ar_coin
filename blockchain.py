import hashlib
import json
from datetime import datetime

from nacl.encoding import HexEncoder
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError


class Wallet:

    def __init__(self, pub_key, name):
        self.pub_key = pub_key
        self.name = name
        self.balance = 0
    
    def serialize(self):
        return {
            'pub_key': self.pub_key,
            'name': self.name,
            'balance': self.balance
        }
    
    def update_balance(self, blockchain):
        self.balance = blockchain.get_wallet_ballance(self.pub_key)


class Transaction:

    def __init__(self, sender, reciever, amount):
        self.sender = sender
        self.reciever = reciever
        self.amount = amount
        self.signature = None
    
    def serialize(self):
        return {
            'sender': self.sender,
            'reciever': self.reciever,
            'amount': self.amount
        }
    
    def calculate_hash(self):
        return hashlib.sha256(json.dumps(self.serialize()).encode()).hexdigest()

    def sign_transaction(self, signing_key):

        if self.sender != str(signing_key.verify_key.encode(encoder=HexEncoder)):
            raise Exception("You can't send money from another one's wallet!")

        hash = self.calculate_hash()
        signed_hash = signing_key.sign(hash.encode(), encoder=HexEncoder)
        self.signature = signed_hash
    
    def transaction_is_valid(self):
        if self.sender == None:
            return True
        if self.signature is None:
            raise Exception("This transaction has not been signed.")
        verify_key = VerifyKey(self.sender.encode(), encoder=HexEncoder)
        signature_bytes = HexEncoder.decode(self.signature.signature)
        try:
            decoded_hash = verify_key.verify(
                self.signature.message,
                signature_bytes,
                encoder=HexEncoder
            )
            if self.calculate_hash() == decoded_hash:
                return True
            return False
        except BadSignatureError:
            return False


class Block:
    
    def __init__(self, previous_hash, transactions, nonce=0):
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.timestamp = datetime.now()
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def serialize_transactions(self):
        transactions = []
        for transaction in self.transactions:
            transactions.append(transaction.serialize())
        return json.dumps(transactions)
    
    def calculate_hash(self):
        data = f"{self.serialize_transactions()}{self.previous_hash}{self.timestamp}{self.nonce}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    def serialize(self):
        return {
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp.strftime("%m/%d/%Y %H:%M:%S.%f"),
            "nonce": self.nonce,
            "hash": self.hash,
            "transactions": [trans.serialize() for trans in self.transactions],
        }
    
    def has_valid_transactions(self):
        for transaction in self.transactions:
            if not transaction.transaction_is_valid():
                return False
        return True


class Blockchain:
    
    def __init__(self, name="Blockchain", pending_transactions=[]):
        print('Building the blockchain...')
        self.name = name
        self.pending_transactions = pending_transactions
        self.block_size = 3
        self.mining_reward = 5
        self.difficulty = 4
        self.chain = [self.create_genesis_block()]
        print('The blockchain is initialized successfully.\n')
    
    def serialize(self):
        return {
            "name": self.name,
            "pending_transactions": [tr.serialize() for tr in self.pending_transactions],
            "chain": [block.serialize() for block in self.chain]
        }
    
    def append_transaction(self, transaction):
        if not transaction.sender or not transaction.reciever:
            raise Exception("Transaction must include a sender and a reciever")
        if not transaction.transaction_is_valid():
            raise Exception("Transaction is not correctly signed.")
        self.pending_transactions.append(transaction)
    
    def create_genesis_block(self):
        genesis_block = Block(
            previous_hash="".join(['0' for i in range(64)]),
            transactions=[
                # {
                #     "Author": "AshesRizer",
                #     "Version": "0.3.2",
                #     "Description": "This blockchain was created for learning perposes only."
                # }
            ]
        )
        # Proof-of-work
        while not genesis_block.hash.startswith(''.join(['0' for i in range(self.difficulty)])):
            genesis_block.nonce += 1
            genesis_block.hash = genesis_block.calculate_hash()
        return genesis_block
    
    def get_latest_block(self):
        return self.chain[-1]
    
    def get_wallet_ballance(self, pub_key):

        balance = 0
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.sender == pub_key:
                    balance -= transaction.amount
                if transaction.reciever == pub_key:
                    balance += transaction.amount
        return balance
    
    def verify_chain_integrity(self):

        for index in range(len(self.chain) - 1, 0, -1):

            if self.chain[index].hash != self.chain[index].calculate_hash():
                print('The chain is invalid.')
                return False
            
            if not self.chain[index].has_valid_transactions():
                print('The transactions in the blockchain are not valid!')
                return False

            if self.chain[index].previous_hash != self.chain[index - 1].hash:
                print('The chain is invalid!')
                return False
        
        return True

    def mine_new_block(self, miner):
        if len(self.pending_transactions) < self.block_size:
            print('Not enough pending transactions.')
            return False
        
        print('mining a new block...')

        new_block = Block(
            previous_hash=self.get_latest_block().hash,
            transactions=self.pending_transactions[:self.block_size]
        )

        # Proof-of-work
        while not new_block.hash.startswith(''.join(['0' for i in range(self.difficulty)])):
            new_block.nonce += 1
            new_block.hash = new_block.calculate_hash()
        
        self.chain.append(new_block)

        if not self.verify_chain_integrity():
            self.chain.remove(new_block)
            return False

        self.pending_transactions = self.pending_transactions[self.block_size:]

        # Create a new transaction to reward the miner
        reward = Transaction(None, miner, self.mining_reward)
        self.append_transaction(reward)

        print("A new block was mined successfully.")
        return True
