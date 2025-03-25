from blockchain import create_genesis_block, mine_block, save_blockchain
from datetime import datetime
import time

# Buat genesis block
genesis_block = create_genesis_block()

# Cetak isi genesis block
print("Genesis Block Created:")
print(f"Index         : {genesis_block.index}")
print(f"Timestamp     : {genesis_block.timestamp} ({datetime.fromtimestamp(genesis_block.timestamp)})")
print(f"Data          : {genesis_block.data}")
print(f"Hash          : {genesis_block.hash}")
print(f"Previous Hash : {genesis_block.previous_hash}")

# Simpan blockchain dalam list
blockchain = [genesis_block]

# Tambah 5 blok baru dengan proses mining
difficulty = 4  # jumlah nol di awal hash

for i in range(1, 6):
    data = f"Block #{i} data"
    print(f"\n⛏️  Mining Block #{i}...")
    start_time = time.time()

    new_block = mine_block(blockchain[-1], data, difficulty)
    blockchain.append(new_block)

    end_time = time.time()
    print(f"✅ Block #{i} mined in {end_time - start_time:.2f} seconds")
    print(f"Hash: {new_block.hash}")

# Cetak seluruh blockchain
print("\n📦 ComCoin Blockchain:")
for block in blockchain:
    print("-" * 50)
    print(f"Index         : {block.index}")
    print(f"Timestamp     : {block.timestamp} ({datetime.fromtimestamp(block.timestamp)})")
    print(f"Data          : {block.data}")
    print(f"Hash          : {block.hash}")
    print(f"Previous Hash : {block.previous_hash}")

# Simpan blockchain ke file JSON
save_blockchain(blockchain)
print("\n📁 Blockchain saved to blockchain.json ✅")
