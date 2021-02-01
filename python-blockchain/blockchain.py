from block import Block

class Blockchain:
  """
  Blockchain: a public ledger of transactions.
    TheImplemented as a list of blocks - data sets of transactions
  """
  def __init__(self):
    self.chain = [] # list of blocks
    
  def add_block(self, data):
    self.chain.append(Block(data))

  def __repr__(self):
    return f'Blockchain: {self.chain}'

blockchain = Blockchain()
blockchain.add_block("ShakespeareOne")
blockchain.add_block("ShakespeareTwo")
blockchain.add_block("ShakespeareThree")

print(blockchain)