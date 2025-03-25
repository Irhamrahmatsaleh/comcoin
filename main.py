from blockchain import (
    create_genesis_block,
    mine_block,
    save_blockchain,
    get_balance,
    validate_transaction,
    Transaction
)
from wallet import (
    generate_key_pair,
    public_key_to_address,
    sign_message
)
from blockchain import load_blockchain
from datetime import datetime
import time
import json
import os

WALLET_FILE = "wallets.json"

def save_wallets():
    with open(WALLET_FILE, "w") as f:
        json.dump(wallets, f, indent=4)

def load_wallets():
    if os.path.exists(WALLET_FILE):
        with open(WALLET_FILE, "r") as f:
            return json.load(f)
    return {}

# Inisialisasi blockchain
blockchain = load_blockchain()
if not blockchain:
    genesis_block = create_genesis_block()
    blockchain = [genesis_block]

# Simpan wallet yang dibuat
wallets = load_wallets()

# Set difficulty
difficulty = 4

def create_wallet():
    priv, pub = generate_key_pair()
    address = public_key_to_address(pub)
    wallets[address] = {
        "private_key": priv,
        "public_key": pub
    }
    save_wallets()
    print(f"\n🔐 Wallet baru dibuat!")
    print(f"Address     : {address}")
    print(f"Private Key : {priv}")
    return address

def view_balance():
    address = input("Masukkan address: ")
    balance = get_balance(address, blockchain)
    print(f"💰 Saldo {address[:10]}...: {balance} CMC")

def send_transaction():
    sender = input("Alamat pengirim       : ")
    recipient = input("Alamat penerima       : ")
    amount = int(input("Jumlah CHIP yang dikirim: "))
    miner_addr = input("Alamat miner (yang akan menerima reward): ")

    if sender not in wallets or miner_addr not in wallets:
        print("⚠️ Address pengirim atau miner belum terdaftar.")
        return

    priv = wallets[sender]["private_key"]
    pub = wallets[sender]["public_key"]

    tx = Transaction(
        sender_address=sender,
        recipient_address=recipient,
        amount=amount,
        sender_public_key=pub
    )
    tx.sign(priv)

    if not validate_transaction(tx, blockchain):
        print("❌ Transaksi tidak valid (signature salah atau saldo tidak cukup).")
        return

    reward_tx = Transaction(
        sender_address="SYSTEM",
        recipient_address=miner_addr,
        amount=50,
        sender_public_key=""
    )

    transactions = [reward_tx, tx]

    print("\n⛏️  Mining block dengan transaksi...")
    new_block = mine_block(blockchain[-1], "Block with transaction", difficulty, transactions)
    blockchain.append(new_block)

    save_blockchain(blockchain)

    print(f"✅ Blok berhasil ditambang! Hash: {new_block.hash}")
    print(f"💰 Saldo pengirim    : {get_balance(sender, blockchain)} CMC")
    print(f"💰 Saldo penerima    : {get_balance(recipient, blockchain)} CMC")
    print(f"💰 Saldo miner       : {get_balance(miner_addr, blockchain)} CMC")

def view_blockchain():
    print("\n📦 ComCoin Blockchain:")
    for block in blockchain:
        print("-" * 50)
        print(f"Index         : {block.index}")
        print(f"Timestamp     : {block.timestamp} ({datetime.fromtimestamp(block.timestamp)})")
        print(f"Hash          : {block.hash}")
        print(f"Previous Hash : {block.previous_hash}")
        for tx in block.transactions:
            print(f"From: {tx.sender_address[:8]}... To: {tx.recipient_address[:8]}... Amount: {tx.amount} CMC")

def menu():
    while True:
        print("\n=== ComCoin CLI ===")
        print("1. Buat Wallet")
        print("2. Lihat Saldo")
        print("3. Kirim CHIP")
        print("4. Lihat Blockchain")
        print("5. Tambang Blok Manual")  # ✅ Pindahkan ke nomor 5
        print("6. Keluar")               # ✅ Pindahkan ke nomor 6
        choice = input("Pilih menu (1-6): ")

        if choice == "1":
            create_wallet()
        elif choice == "2":
            view_balance()
        elif choice == "3":
            send_transaction()
        elif choice == "4":
            view_blockchain()
        elif choice == "5":
            miner_addr = input("Masukkan address wallet untuk menerima reward: ")

            if miner_addr not in wallets:
                print("❌ Address tidak ditemukan di wallets.json. Mining ditolak.")
                continue

            reward_tx = Transaction(
                sender_address="SYSTEM",
                recipient_address=miner_addr,
                amount=50,
                sender_public_key=""
            )
            transactions = [reward_tx]

            print("\n⛏️ Menambang blok untuk reward...")
            new_block = mine_block(blockchain[-1], "Reward block", difficulty, transactions)
            blockchain.append(new_block)

            save_blockchain(blockchain)
            print(f"✅ Blok ditambang! Hash: {new_block.hash}")
            print(f"💰 Saldo {miner_addr[:10]}... sekarang: {get_balance(miner_addr, blockchain)} CMC")
            print("💾 Blockchain disimpan ke blockchain.json ✅")

        elif choice == "6":
            save_blockchain(blockchain)
            save_wallets()
            print("📁 Blockchain & Wallets disimpan. Keluar...")
            break
        else:
            print("❌ Menu tidak tersedia.")

# Jalankan CLI
menu()
