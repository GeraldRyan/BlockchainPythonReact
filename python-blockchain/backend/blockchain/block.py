import time

from backend.util.crypto_hash import crypto_hash
from backend.util.hex_to_binary import hex_to_binary
from backend.config import MINE_RATE

GENESIS_DATA = {
    'timestamp': 1,
    'last_hash': 'genesis_last_hash',
    'hash': 'genesis_hash',
    'data': [],
    'difficulty': 3,
    'nonce': 'genesis_nonce',
    'last_block': None
}


class Block:
    """
    Block: a unit of storage.
    Store transactions in a blockchain that supports a cryptocurrency.
    """

    def __init__(self, timestamp, last_hash, hash, data, difficulty, nonce, last_block=None):
        self.timestamp = timestamp
        self.last_hash = last_hash
        self.hash = hash
        self.data = data
        self.difficulty = difficulty
        self.nonce = nonce
        self.last_block = last_block

    def __repr__(self):
        return (
            'Block('
            f'timestamp: {self.timestamp}, '
            f'last_hash: {self.last_hash}, '
            f'hash: {self.hash}, '
            f'data: {self.data}, '
            f'difficulty: {self.difficulty}, '
            f'nonce: {self.nonce})'
        )

    @staticmethod
    def mine_block(last_block, data):
        """
        Mine a block based on the given last_block and data until a block hash is found that meets the leading 0's POW requirement.
        """
        timestamp = time.time_ns()
        last_hash = last_block.hash
        if last_block.last_block == None:
            second_last_timestamp = last_block.timestamp
        else:
            second_last_timestamp = last_block.last_block.timestamp

        difficulty = Block.adjust_difficulty(last_block, second_last_timestamp)
        nonce = 0
        hash = crypto_hash(timestamp, last_hash, data, difficulty, nonce)

        while hex_to_binary(hash)[0:difficulty] != '0' * difficulty:
            nonce += 1
            timestamp = time.time_ns()
            hash = crypto_hash(timestamp, last_hash, data, difficulty, nonce)
        return Block(timestamp, last_hash, hash, data, difficulty, nonce, last_block)

    @staticmethod
    def genesis():
        """
        generate genesis block
        """
        return Block(**GENESIS_DATA)

    @staticmethod
    def adjust_difficulty(last_block, second_last_timestamp):
        '''
        Calculate the adjusted difficulty according to the MINE_RATE.
        Increase the difficulty for quickly mined blocks. 
        Decrease the difficulty for slowly mined blocks. 
        '''
        time_diff = last_block.timestamp - second_last_timestamp
        if (time_diff) < MINE_RATE:
            print("Difficulty increasing")
            return last_block.difficulty + 1

        if (last_block.difficulty - 1) > 0:
            print("Difficulty DECREASING")
            return last_block.difficulty - 1
        return 1


def main():

    genesis_block = Block.genesis()
    block = Block.mine_block(genesis_block, 'Shakespeare')
    print(block)
    print(Block.mine_block(genesis_block, 'Goodbye Norma Jean'))
    print(Block.mine_block(genesis_block, 'Goodbye Elmer Fudd'))


if __name__ == '__main__':
    main()
