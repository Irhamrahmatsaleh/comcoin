import unittest
from comcoin.block import Block


class TestBlock(unittest.TestCase):
    def test_block_hash(self):
        block = Block(0, [], "0")
        original_hash = block.hash
        block.nonce += 1
        new_hash = block.compute_hash()
        self.assertNotEqual(original_hash, new_hash)


if __name__ == '__main__':
    unittest.main()
