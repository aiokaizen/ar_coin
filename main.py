from datetime import datetime
import hashlib
import json


class Wallet:

    def __init__(self, pub_key, name, balance):
        self.pub_key = pub_key
        self.name = name
        self.balance = balance
    
    def as_dict(self):
        return {
            'pub_key': self.pub_key,
            'name': self.name,
            'balance': self.balance
        }


class Transaction:

    def __init__(self, sender, reciever, amount):
        self.sender = sender
        self.reciever = reciever
        self.amount = amount
    
    def as_dict(self):
        return {
            'sender': self.sender.as_dict(),
            'reciever': self.reciever.as_dict(),
            'amount': self.amount
        }
    
    def execute(self):
        if not self.is_valid():
            return False
        
        self.sender.balance -= self.amount
        self.reciever.balance += self.amount
        return True


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
            transactions.append(transaction.as_dict())
        return json.dumps(transactions)
    
    def serialize(self):
        return {
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp.strftime("%m/%d/%Y %H:%M:%S.%f"),
            "nonce": self.nonce,
            "hash": self.hash,
            "transactions": [trans.as_dict() for trans in self.transactions],
        }
    
    def calculate_hash(self):
        data = f"{self.serialize_transactions()}{self.previous_hash}{self.timestamp}{self.nonce}"
        return hashlib.sha256(data.encode()).hexdigest()


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
            "pending_transactions": [tr.as_dict() for tr in self.pending_transactions],
            "chain": [block.serialize() for block in self.chain]
        }
    
    def get_latest_block(self):
        return self.chain[-1]
    
    def verify_chain_integrity(self):

        for index in range(len(self.chain) - 1, 0, -1):

            if self.chain[index].hash != self.chain[index].calculate_hash():
                print('The chain is invalid.')
                return False

            if self.chain[index].previous_hash != self.chain[index - 1].hash:
                print('The chain is invalid!')
                return False
        
        return True
    
    def create_genesis_block(self):
        genesis_block = Block(
            previous_hash="".join(['0' for i in range(64)]),
            transactions=[]
        )
        # Proof-of-work
        while not genesis_block.hash.startswith(''.join(['0' for i in range(self.difficulty)])):
            genesis_block.nonce += 1
            genesis_block.hash = genesis_block.calculate_hash()
        return genesis_block

    def mine_new_block(self, miner):
        if len(self.pending_transactions) < 3:
            print('Not enough transactions.')
            return False
        
        print('mining a new block...')

        new_block = Block(
            previous_hash=self.get_latest_block().hash,
            transactions=self.pending_transactions[:3]
        )

        # Proof-of-work
        while not new_block.hash.startswith(''.join(['0' for i in range(self.difficulty)])):
            new_block.nonce += 1
            new_block.hash = new_block.calculate_hash()
        
        self.chain.append(new_block)

        if not self.verify_chain_integrity():
            self.chain.remove(new_block)
            return False

        self.pending_transactions = self.pending_transactions[3:]

        miner.balance += self.mining_reward

        print("A new block was mined successfully.")
        return True
