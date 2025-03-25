from ecdsa import SigningKey, SECP256k1


class Wallet:
    def __init__(self):
        self.private_key = SigningKey.generate(curve=SECP256k1)
        self.public_key = self.private_key.get_verifying_key()

    def get_private_key(self):
        """
        Return private key as hex string.
        """
        return self.private_key.to_string().hex()

    def get_public_key(self):
        """
        Return public key as hex string.
        """
        return self.public_key.to_string().hex()

    @staticmethod
    def load_wallet_from_private_key(private_key_hex):
        """
        Recreate wallet from an existing private key.
        """
        private_key = SigningKey.from_string(bytes.fromhex(private_key_hex), curve=SECP256k1)
        wallet = Wallet.__new__(Wallet)  # bypass __init__
        wallet.private_key = private_key
        wallet.public_key = private_key.get_verifying_key()
        return wallet
