import requests
from comcoin.wallet import Wallet
from comcoin.transaction import Transaction


def main():
    print("💸 Send ComCoin Transaction")

    private_key = input("🔐 Sender's Private Key: ").strip()
    recipient = input("🏦 Recipient's Public Key: ").strip()
    amount = float(input("💰 Amount to send: ").strip())

    # Buat wallet dari private key
    sender_wallet = Wallet.load_wallet_from_private_key(private_key)
    sender_pub = sender_wallet.get_public_key()

    # Buat transaksi dan tanda tangani
    tx = Transaction(sender=sender_pub, recipient=recipient, amount=amount)
    tx.sign_transaction(private_key)

    # Kirim ke node
    response = requests.post("http://localhost:5000/new_transaction", json=vars(tx))

    if response.status_code == 201:
        print("✅ Transaction sent successfully!")
    else:
        print(f"❌ Error: {response.text}")


if __name__ == "__main__":
    main()
