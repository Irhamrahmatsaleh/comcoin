from comcoin.wallet import Wallet

def main():
    wallet = Wallet()
    private_key = wallet.get_private_key()
    public_key = wallet.get_public_key()

    print("🎉 New ComCoin Wallet Created!")
    print(f"🔐 Private Key:  {private_key}")
    print(f"🏦 Public Key:   {public_key}")
    print("\n⚠️  Keep your private key safe! If you lose it, you lose access to your coins.")

if __name__ == "__main__":
    main()
