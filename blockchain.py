import hashlib
import time
import json
from wallet import sign_message, verify_signature

class Block:
    def __init__(self, index, previous_hash, timestamp, data, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.previous_hash}{self.timestamp}{self.data}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()

def create_genesis_block():
    """
    Membuat Genesis Block (blok pertama dalam blockchain)
    """
    return Block(0, "0", int(time.time()), "Genesis Block")

def create_new_block(previous_block, data):
    """
    Fungsi biasa untuk membuat blok baru tanpa proses mining
    """
    index = previous_block.index + 1
    timestamp = int(time.time())
    previous_hash = previous_block.hash
    return Block(index, previous_hash, timestamp, data)

def mine_block(previous_block, data, difficulty=4):
    """
    Mining blok baru dengan mencari nonce sampai hash-nya diawali sejumlah nol tertentu (difficulty)
    """
    prefix = '0' * difficulty
    nonce = 0
    timestamp = int(time.time())

    while True:
        block = Block(
            index=previous_block.index + 1,
            previous_hash=previous_block.hash,
            timestamp=timestamp,
            data=data,
            nonce=nonce
        )
        if block.hash.startswith(prefix):
            return block
        nonce += 1

# Transaksi
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
        if self.sender_address == "SYSTEM":  # reward mining, tidak perlu signature
            return True
        if not self.signature:
            return False
        return verify_signature(self.sender_public_key, self.to_message(), self.signature)

# json
def save_blockchain(blockchain, filename="blockchain.json"):
    data = []
    for block in blockchain:
        block_data = {
            "index": block.index,
            "timestamp": block.timestamp,
            "data": block.data,
            "previous_hash": block.previous_hash,
            "nonce": block.nonce,
            "hash": block.hash
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
                block = Block(
                    index=block_data["index"],
                    previous_hash=block_data["previous_hash"],
                    timestamp=block_data["timestamp"],
                    data=block_data["data"],
                    nonce=block_data["nonce"]
                )
                blockchain.append(block)
            return blockchain
    except FileNotFoundError:
        return []
