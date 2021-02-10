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
  print("XXXXXXXXXXXXXXXXXXXX\n")
  blockchain_json = blockchain.to_json()
  print(blockchain_json)
  blockchain_jsonified = jsonify(blockchain_json)
  print("XXXXXXXXXXXXXXXXXXXX\n")
  print("XXXXXXXXXXXXXXXXXXXX\n")
  print(blockchain_jsonified)

  return blockchain_jsonified

  # return jsonify(blockchain.to_json())


app.run()