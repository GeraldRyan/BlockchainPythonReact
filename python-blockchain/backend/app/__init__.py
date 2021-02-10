from flask import Flask, jsonify

from backend.blockchain.blockchain import Blockchain

app = Flask(__name__)
blockchain = Blockchain()

for i in range(5):
  blockchain.add_block(i)




@app.route("/")
def route_default():
  return "<h1 style='color:green'>Welcome to the Blockchain!</h1>"

@app.route("/blockchain")
def route_blockchain():
  return jsonify(blockchain.to_json())


app.run()