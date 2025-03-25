from comcoin.transaction import Transaction
from comcoin.wallet import Wallet
from comcoin.blockchain import Blockchain


class Miner:
    def __init__(self, blockchain, reward=50):
        self.blockchain = blockchain
        self.reward = reward

    def mine_pending_transactions(self, miner_public_key_hex):
        """
        Tambahkan reward transaction lalu tambahkan block ke blockchain.
        """
        # Tambahkan reward transaksi dari 'SYSTEM' ke miner
        reward_tx = Transaction("SYSTEM", miner_public_key_hex, self.reward)
        self.blockchain.add_new_transaction(vars(reward_tx))

        # Proses mining (proof of work)
        mined_index = self.blockchain.mine()
        return mined_index
