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
    NUMBER = 2

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

    def __eq__(self, other):
        if (other is not None):
            return self.__dict__ == other.__dict__
        return False

    def to_json(self):
        '''
        Serialize the block into a dictionary of its attributes
        Note, at the moment the last_block is being dropped from the response.
        Should it prove to be necessary for the blockchain network, we will restore it back and serialize it.
        '''


        block_as_dict = self.__dict__
        if "last_block" in block_as_dict:
            block_as_dict.pop("last_block")
        return block_as_dict
        # block_as_dict = self.__dict__
        # if self.last_block != None:
        #     block_as_dict["last_block"] = self.last_block.__dict__
        # return block_as_dict

    @staticmethod
    def mine_block(last_block, data):
        """
        Mine a block based on the given last_block and data until a block hash is found that meets the leading 0's POW requirement.
        """
        timestamp = time.time_ns()
        last_hash = last_block.hash
        if last_block.last_block == None:  # if block #2
            difficulty = 4  # second block and no need to call adjust.
        elif last_block.last_block.last_block == None:
            difficulty = 5
        else:
            second_last_timestamp = last_block.last_block.timestamp
            difficulty = Block.adjust_difficulty(
                last_block, second_last_timestamp)
        nonce = 0
        hash = crypto_hash(timestamp, last_hash, data, difficulty, nonce)

        while hex_to_binary(hash)[0:difficulty] != '0' * difficulty:
            nonce += 1
            timestamp = time.time_ns()
            hash = crypto_hash(timestamp, last_hash, data, difficulty, nonce)
        # print(f"Block {Block.NUMBER} mined. Difficulty:{difficulty}\n\n")
        Block.NUMBER += 1
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
        # print(f"Block time difference:{time_diff/1000000000}")
        if (time_diff) < MINE_RATE:
            print("Difficulty increasing")
            return last_block.difficulty + 1

        if (last_block.difficulty - 1) > 0:
            print("Difficulty DECREASING")
            return last_block.difficulty - 1
        return 1

    @staticmethod
    def is_valid_block(last_block, block):
        '''
        Validate a block by enforcing the following rules:
        - the block must have the proper last_hash reference
        - the block must meet the proof of work requirement
        - the difficulty must only adjust by one
        - the block hash must be a valid combination of the block fields
        '''

        if block.last_hash != last_block.hash:
            raise Exception('The block last_hash must be correct')
        if hex_to_binary(block.hash)[0:block.difficulty] != '0' * block.difficulty:
            raise Exception('The proof of work requirement was not met')
        if abs(last_block.difficulty - block.difficulty) > 1:
            raise Exception('The block difficulty must only adjust by 1')

        reconstructed_hash = crypto_hash(
            block.timestamp,
            block.last_hash,
            block.data,
            block.nonce,
            block.difficulty,
            # block.last_block # Not necessary or used in hash function. It's part of object but is not put into hash
        )
        if block.hash != reconstructed_hash:
            raise Exception('The block hash must be correct')


def main():
    genesis_block = Block.genesis()
    bad_block = Block.mine_block(genesis_block, 'foo')
    bad_block.last_hash = 'evil_data'  # TOGGLE ME good block/bad block
    try:
        Block.is_valid_block(genesis_block, bad_block)
    except Exception as e:  # means only exception message is displayed in console.
        print(f'is_valid_block: {e}')
    print("BLOCK DICT")
    print(bad_block.__dict__)
    print("BLOCK SERIALIZED (TO JSON)")
    print(bad_block.to_json())


if __name__ == '__main__':
    main()
