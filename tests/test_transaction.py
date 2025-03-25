import unittest
from comcoin.wallet import Wallet
from comcoin.transaction import Transaction


class TestTransaction(unittest.TestCase):
    def test_signature_and_validation(self):
        wallet = Wallet()
        tx = Transaction(wallet.get_public_key(), "recipient", 10)
        tx.sign_transaction(wallet.get_private_key())
        self.assertTrue(tx.is_valid())

    def test_invalid_signature(self):
        wallet1 = Wallet()
        wallet2 = Wallet()
        tx = Transaction(wallet1.get_public_key(), "recipient", 10)
        tx.sign_transaction(wallet2.get_private_key())  # salah private key
        self.assertFalse(tx.is_valid())


if __name__ == '__main__':
    unittest.main()
