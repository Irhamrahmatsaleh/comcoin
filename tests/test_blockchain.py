import unittest
from comcoin.blockchain import Blockchain


class TestBlockchain(unittest.TestCase):
    def test_add_transaction_and_mine(self):
        bc = Blockchain()
        self.assertEqual(len(bc.chain), 1)  # Genesis block

        tx = {"sender": "a", "recipient": "b", "amount": 10}
        bc.add_new_transaction(tx)
        bc.mine()

        self.assertEqual(len(bc.chain), 2)  # Block mined
        self.assertEqual(bc.chain[1].transactions[0]["sender"], "a")


if __name__ == '__main__':
    unittest.main()
