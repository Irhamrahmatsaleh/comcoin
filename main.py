from blockchain import create_genesis_block

# Buat genesis block
genesis_block = create_genesis_block()

# Cetak isi genesis block
print("Genesis Block Created:")
print(f"Index         : {genesis_block.index}")
print(f"Timestamp     : {genesis_block.timestamp}")
print(f"Data          : {genesis_block.data}")
print(f"Hash          : {genesis_block.hash}")
print(f"Previous Hash : {genesis_block.previous_hash}")
