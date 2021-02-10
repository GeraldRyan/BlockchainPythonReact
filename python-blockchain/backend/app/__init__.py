from flask import Flask, jsonify

from backend.blockchain.blockchain import Blockchain

app = Flask(__name__)
blockchain = Blockchain()

@app.route("/")
def route_default():
  return "<h1 style='color:green'>Welcome to the Blockchain!</h1>"

@app.route("/blockchain/")
def route_blockchain():
  return jsonify(blockchain.to_json())

@app.route("/blockchain/mine/")
def route_blockchain_mine():
  transaction_data = "stubbed_transaction_data"

  blockchain.add_block(transaction_data)

  return jsonify(blockchain.chain[-1].to_json())



app.run()