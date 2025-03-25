from wallet import generate_key_pair, public_key_to_address, sign_message, verify_signature
from blockchain import (
    Transaction,
    Block,
    mine_block,
    save_blockchain,
    create_genesis_block,
    get_balance,
    validate_transaction
)
from datetime import datetime

# Buat wallet pengirim & penerima
priv1, pub1 = generate_key_pair()
addr1 = public_key_to_address(pub1)

priv2, pub2 = generate_key_pair()
addr2 = public_key_to_address(pub2)

# Buat wallet miner (penerima reward)
miner_priv, miner_pub = generate_key_pair()
miner_addr = public_key_to_address(miner_pub)

# Buat Genesis Block
genesis_block = create_genesis_block()
blockchain = [genesis_block]

# 🧾 Tampilkan saldo sebelum transaksi
balance_before = get_balance(addr1, blockchain)
print(f"\n💰 Saldo {addr1[:8]}... sebelum transaksi: {balance_before} CMC")

# Transaksi utama: addr1 kirim 15 CMC ke addr2
tx1 = Transaction(
    sender_address=addr1,
    recipient_address=addr2,
    amount=15,
    sender_public_key=pub1
)
tx1.sign(priv1)

# Transaksi reward untuk miner (coinbase)
reward_tx = Transaction(
    sender_address="SYSTEM",
    recipient_address=addr1,  # Kirim reward ke addr1 dulu agar cukup saldo
    amount=50,
    sender_public_key=""
)

# Validasi sebelum blok ditambang
print("✅ Validasi transaksi sebelum mining:", validate_transaction(tx1, blockchain))

# Masukkan reward dulu agar addr1 bisa mengirim
transactions = [reward_tx, tx1]

# Mining blok baru dengan transaksi
print("\n⛏️ Mining block with transactions...")
new_block = mine_block(
    previous_block=genesis_block,
    data="Block with transactions",
    difficulty=4,
    transactions=transactions
)
blockchain.append(new_block)

# Cetak hasil blok
print("\n✅ Block Mined:")
print("-" * 50)
print(f"Index         : {new_block.index}")
print(f"Timestamp     : {new_block.timestamp} ({datetime.fromtimestamp(new_block.timestamp)})")
print(f"Hash          : {new_block.hash}")
print(f"Previous Hash : {new_block.previous_hash}")
print("📄 Transactions:")
for tx in new_block.transactions:
    print(f"From: {tx.sender_address[:8]}... To: {tx.recipient_address[:8]}... Amount: {tx.amount} CMC")

# 🧾 Tampilkan saldo setelah transaksi
balance_after_sender = get_balance(addr1, blockchain)
balance_after_receiver = get_balance(addr2, blockchain)

print(f"\n💰 Saldo {addr1[:8]}... setelah transaksi: {balance_after_sender} CMC")
print(f"💰 Saldo {addr2[:8]}... setelah transaksi: {balance_after_receiver} CMC")

# Simpan blockchain ke file
save_blockchain(blockchain)
print("\n💾 Blockchain saved to blockchain.json ✅")
