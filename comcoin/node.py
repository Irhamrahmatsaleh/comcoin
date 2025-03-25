from flask import Flask, request, jsonify
from flask_cors import CORS  # 👉 Tambahkan untuk support frontend (UI)
import requests

from comcoin.blockchain import Blockchain
from comcoin.transaction import Transaction
from comcoin.wallet import Wallet
from comcoin.miner import Miner
from comcoin.block import Block  # digunakan di sync_chain

app = Flask(__name__)
CORS(app)  # 👉 Aktifkan CORS

blockchain = Blockchain()
miner = Miner(blockchain)
peers = set()


@app.route('/create_wallet', methods=['GET'])
def create_wallet():
    wallet = Wallet()
    return jsonify({
        "private_key": wallet.get_private_key(),
        "public_key": wallet.get_public_key()
    })

# Endpoint untuk melihat saldo berdasarkan public key
@app.route('/get_balance', methods=['POST'])
def get_balance():
    data = request.get_json()
    public_key = data.get("public_key")
    if not public_key:
        return jsonify({"error": "Public key is required"}), 400

    balance = 0
    for block in blockchain.chain:
        for tx in block.transactions:
            if tx["recipient"] == public_key:
                balance += tx["amount"]
            if tx["sender"] == public_key:
                balance -= tx["amount"]

    return jsonify({"balance": balance})

# Endpoint untuk melihat histori transaksi
@app.route('/get_transactions', methods=['POST'])
def get_transactions():
    data = request.get_json()
    public_key = data.get("public_key")
    if not public_key:
        return jsonify({"error": "Public key is required"}), 400

    transactions = []
    for block in blockchain.chain:
        for tx in block.transactions:
            if tx["recipient"] == public_key or tx["sender"] == public_key:
                transactions.append(tx)

    return jsonify({"transactions": transactions})



@app.route('/get_public_key', methods=['POST'])
def get_public_key():
    data = request.get_json()
    private_key = data.get("private_key")
    if not private_key:
        return jsonify({"error": "Private key is required"}), 400
    wallet = Wallet.load_wallet_from_private_key(private_key)
    return jsonify({"public_key": wallet.get_public_key()})


@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append({
            "index": block.index,
            "transactions": block.transactions,
            "timestamp": block.timestamp,
            "previous_hash": block.previous_hash,
            "nonce": block.nonce,
            "hash": block.hash
        })
    return jsonify({"length": len(chain_data), "chain": chain_data})


@app.route('/pending', methods=['GET'])
def get_pending_transactions():
    return jsonify(blockchain.unconfirmed_transactions)


@app.route('/new_transaction', methods=['POST'])
def new_transaction():
    tx_data = request.get_json()
    required_fields = ["sender", "recipient", "amount", "signature"]

    if not all(field in tx_data for field in required_fields):
        return "Invalid transaction data", 400

    tx = Transaction(tx_data["sender"], tx_data["recipient"], tx_data["amount"], tx_data["signature"])
    if not tx.is_valid():
        return "Invalid transaction signature", 400

    blockchain.add_new_transaction(vars(tx))
    return "Transaction added successfully", 201


@app.route('/mine', methods=['POST'])
def mine_block():
    data = request.get_json()
    if "miner_address" not in data:
        return "Missing miner address", 400

    index = miner.mine_pending_transactions(data["miner_address"])
    if index is False:
        return "No transactions to mine", 400

    return f"Block #{index} mined successfully", 200


@app.route('/add_peer', methods=['POST'])
def add_peer():
    peer_data = request.get_json()
    peer = peer_data.get("peer")
    if not peer:
        return "Invalid peer data", 400

    peers.add(peer)
    return "Peer added", 201


@app.route('/peers', methods=['GET'])
def get_peers():
    return jsonify(list(peers))


@app.route('/sync', methods=['GET'])
def sync_chain():
    global blockchain
    longest_chain = None
    max_length = len(blockchain.chain)

    for peer in peers:
        try:
            response = requests.get(f"{peer}/chain")
            length = response.json()["length"]
            chain = response.json()["chain"]
            if length > max_length:
                max_length = length
                longest_chain = chain
        except Exception:
            continue

    if longest_chain:
        new_chain = []
        for block_data in longest_chain:
            block = Block(
                block_data["index"],
                block_data["transactions"],
                block_data["previous_hash"],
                block_data["nonce"],
                block_data["timestamp"]
            )
            block.hash = block_data["hash"]
            new_chain.append(block)
        blockchain.chain = new_chain
        return "Chain replaced with longer one", 200
    return "Current chain is the longest", 200
