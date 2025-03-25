import hashlib
import time
import json
from wallet import sign_message, verify_signature

# ------------------------------------
# TRANSACTION
# ------------------------------------

class Transaction:
    def __init__(self, sender_address, recipient_address, amount, sender_public_key):
        self.sender_address = sender_address
        self.recipient_address = recipient_address
        self.amount = amount
        self.sender_public_key = sender_public_key
        self.signature = None

    def to_message(self):
        return f"{self.sender_address}->{self.recipient_address}:{self.amount}"

    def sign(self, private_key):
        self.signature = sign_message(private_key, self.to_message())

    def is_valid(self):
        if self.sender_address == "SYSTEM":
            return True  # coinbase tx doesn't need signature
        if not self.signature:
            return False
        return verify_signature(self.sender_public_key, self.to_message(), self.signature)

# ------------------------------------
# BLOCK
# ------------------------------------

class Block:
    def __init__(self, index, previous_hash, timestamp, data, nonce=0, transactions=None):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.nonce = nonce
        self.transactions = transactions or []
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        tx_data = "".join([tx.to_message() for tx in self.transactions])
        block_string = f"{self.index}{self.previous_hash}{self.timestamp}{self.data}{tx_data}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()

# ------------------------------------
# BLOCKCHAIN CORE
# ------------------------------------

def create_genesis_block():
    return Block(0, "0", int(time.time()), "Genesis Block")

def create_new_block(previous_block, data):
    index = previous_block.index + 1
    timestamp = int(time.time())
    previous_hash = previous_block.hash
    return Block(index, previous_hash, timestamp, data)

def mine_block(previous_block, data, difficulty=4, transactions=None):
    prefix = '0' * difficulty
    nonce = 0
    timestamp = int(time.time())

    while True:
        block = Block(
            index=previous_block.index + 1,
            previous_hash=previous_block.hash,
            timestamp=timestamp,
            data=data,
            nonce=nonce,
            transactions=transactions
        )
        if block.hash.startswith(prefix):
            return block
        nonce += 1

# ------------------------------------
# BALANCE / UTXO
# ------------------------------------

def get_balance(address, blockchain):
    balance = 0
    for block in blockchain:
        for tx in block.transactions:
            if tx.sender_address == address and tx.sender_address != "SYSTEM":
                balance -= tx.amount
            if tx.recipient_address == address:
                balance += tx.amount
    return balance

def validate_transaction(tx, blockchain):
    if not tx.is_valid():
        return False
    if tx.sender_address == "SYSTEM":
        return True  # mining reward
    sender_balance = get_balance(tx.sender_address, blockchain)
    return sender_balance >= tx.amount

# ------------------------------------
# JSON I/O
# ------------------------------------

def save_blockchain(blockchain, filename="blockchain.json"):
    data = []
    for block in blockchain:
        block_data = {
            "index": block.index,
            "timestamp": block.timestamp,
            "data": block.data,
            "previous_hash": block.previous_hash,
            "nonce": block.nonce,
            "hash": block.hash,
            "transactions": [
                {
                    "sender": tx.sender_address,
                    "recipient": tx.recipient_address,
                    "amount": tx.amount,
                    "signature": tx.signature
                } for tx in block.transactions
            ]
        }
        data.append(block_data)

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def load_blockchain(filename="blockchain.json"):
    try:
        with open(filename, "r") as f:
            data = json.load(f)
            blockchain = []
            for block_data in data:
                txs = []
                for tx in block_data.get("transactions", []):
                    transaction = Transaction(
                        sender_address=tx["sender"],
                        recipient_address=tx["recipient"],
                        amount=tx["amount"],
                        sender_public_key=""  # opsional, karena tidak disimpan
                    )
                    transaction.signature = tx["signature"]
                    txs.append(transaction)
                block = Block(
                    index=block_data["index"],
                    previous_hash=block_data["previous_hash"],
                    timestamp=block_data["timestamp"],
                    data=block_data["data"],
                    nonce=block_data["nonce"],
                    transactions=txs
                )
                blockchain.append(block)
            return blockchain
    except FileNotFoundError:
        return []
