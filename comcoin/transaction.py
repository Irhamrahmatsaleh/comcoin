import json
import hashlib
from ecdsa import SigningKey, VerifyingKey, SECP256k1


class Transaction:
    def __init__(self, sender, recipient, amount, signature=None):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.signature = signature

    def to_dict(self):
        return {
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': self.amount
        }

    def compute_hash(self):
        """
        Compute the SHA-256 hash of the transaction.
        """
        tx_str = json.dumps(self.to_dict(), sort_keys=True).encode()
        return hashlib.sha256(tx_str).hexdigest()

    def sign_transaction(self, private_key_str):
        """
        Sign transaction using sender's private key (in hex).
        """
        private_key = SigningKey.from_string(bytes.fromhex(private_key_str), curve=SECP256k1)
        tx_hash = self.compute_hash()
        self.signature = private_key.sign(tx_hash.encode()).hex()

    def is_valid(self):
        """
        Verify signature using sender's public key.
        """
        if self.sender == "SYSTEM":  # Reward transactions
            return True
        if not self.signature:
            return False
        try:
            public_key = VerifyingKey.from_string(bytes.fromhex(self.sender), curve=SECP256k1)
            tx_hash = self.compute_hash()
            return public_key.verify(bytes.fromhex(self.signature), tx_hash.encode())
        except Exception:
            return False
