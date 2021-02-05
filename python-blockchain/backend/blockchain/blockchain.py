from backend.blockchain.block import Block

class Blockchain:
  """
  Blockchain: a public ledger of transactions.
    TheImplemented as a list of blocks - data sets of transactions
  """
  def __init__(self):
    self.chain = [Block.genesis()] # list of blocks
    
  def add_block(self, data):
    self.chain.append(Block.mine_block(self.chain[-1], data))

  def __repr__(self):
    return f'Blockchain: {self.chain}'

def main():
  blockchain = Blockchain()
  blockchain.add_block("ShakespeareOne")
  blockchain.add_block("ShakespeareTwo")
  blockchain.add_block("ShakespeareThree")

  print(blockchain) 
  print(f'blockchain.py __name__: {__name__}')

if __name__ == '__main__':
  main()