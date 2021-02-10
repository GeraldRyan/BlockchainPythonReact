from backend.blockchain.block import Block
from flask import Flask, jsonify

class Blockchain:
    """
    Blockchain: a public ledger of transactions.
      TheImplemented as a list of blocks - data sets of transactions
    """

    def __init__(self):
        self.chain = [Block.genesis()]  # list of blocks

    def add_block(self, data):
        self.chain.append(Block.mine_block(self.chain[-1], data))

    def __repr__(self):
        return f'Blockchain: {self.chain}'

    def replace_chain(self, chain):
        '''
        Replace the local chain with the incoming chain if the following apply:
          - The incoming chain is longer than the local one.
          - The incoming chain is formatted properly.
        '''
        if len(chain) <= len(self.chain):
            raise Exception(
                'Cannot replace chain. The incoming chain must be longer.')

        try:
            Blockchain.is_valid_chain(chain)
        except Exception as e:
            raise Exception(
                f'Cannot replace. The incoming chain is invalid: {e}')

        self.chain = chain

    def to_json(self):
      '''
      Serialize the blockchain into a list of blocks.
      '''
      return list(map(lambda block: block.to_json(), self.chain)) 

    @staticmethod
    def is_valid_chain(chain):
        '''
        Validate the incoming chain.
        Enforce the following rules of the blockchain:
          - the chain must start with the genesis block
          - blocks must be formatted correctly
        '''

        if chain[0] != Block.genesis():
            raise Exception('The genesis block must be valid')

        for i in range(1, len(chain)):
            block = chain[i]
            last_block = chain[i-1]
            Block.is_valid_block(last_block, block)


def main():
    blockchain = Blockchain()
    blockchain.add_block("ShakespeareOne")
    blockchain.add_block("ShakespeareTwo")
    blockchain.add_block("ShakespeareThree")

    print(blockchain.to_json())
    print(f'blockchain.py __name__: {__name__}')


if __name__ == '__main__':
    main()
