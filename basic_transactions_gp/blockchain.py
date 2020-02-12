# Paste your version of blockchain.py from the client_mining_p
# folder here

import hashlib
import json
from time import time
from uuid import uuid4

from flask import Flask, jsonify, request


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Create the genesis block
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        Create a new Block in the Blockchain

        A block should have:
        * Index
        * Timestamp
        * List of current transactions
        * The proof used to mine this block
        * The hash of the previous block

        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """

        block = {
            "index": len(self.chain) + 1,
            "timestamp": time(),
            "transactions": self.current_transactions,
            "proof": proof,
            "previous_hash": previous_hash


        }

        # Reset the current list of transactions
        self.current_transactions = []
        # Append the chain to the block
        self.chain.append(block)
        # Return the new block
        return block

    def hash(self, block):
        """
        Creates a SHA-256 hash of a Block

        :param block": <dict> Block
        "return": <str>
        """

        # Use json.dumps to convert json into a string
        # Use hashlib.sha256 to create a hash
        # It requires a `bytes-like` object, which is what
        # .encode() does.
        # It converts the Python string into a byte string.
        # We must make sure that the Dictionary is Ordered,
        # or we'll have inconsistent hashes

        # TODO: Create the block_string
        string_object = json.dumps(block, sort_keys=True).encode()

        # TODO: Hash this string using sha256
        raw_hash = hashlib.sha256(string_object)
        # By itself, the sha256 function returns the hash in a raw string
        # that will likely include escaped characters.
        # This can be hard to read, but .hexdigest() converts the
        # hash to a string of hexadecimal characters, which is
        # easier to work with and understand

        # TODO: Return the hashed block string in hexadecimal format

        hex_hash = raw_hash.hexdigest()
        return hex_hash

    def new_transaction(self, sender, recipient, amount):

        transaction = {"sender": sender,
                       "recipient": recipient, "amount": amount}
        self.current_transactions.append(transaction)

        return self.last_block["index"] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    # def proof_of_work(self, block):
    #     """
    #     Simple Proof of Work Algorithm
    #     Stringify the block and look for a proof.
    #     Loop through possibilities, checking each one against `valid_proof`
    #     in an effort to find a number that is a valid proof
    #     :return: A valid proof for the provided block
    #     """
    #     # TODO
    #     block_string = json.dumps(block)
    #     proof = 0

    #     while not self.valid_proof(block_string, proof):
    #         proof = proof + 1

    #     return proof

        # return proof

    @staticmethod
    def valid_proof(block_string, proof):
        """
        Validates the Proof:  Does hash(block_string, proof) contain 6
        leading zeroes?  Return true if the proof is valid
        :param block_string: <string> The stringified block to use to
        check in combination with `proof`
        :param proof: <int?> The value that when combined with the
        stringified previous block results in a hash that has the
        correct number of leading zeroes.
        :return: True if the resulting hash is a valid proof, False otherwise
        """
        # TODO
        guess = f"{block_string}{proof}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()

        # True if the combination of the last block + proof hash contains 6 leading zeros
        # False if it not
        return guess_hash[:6] == "0"*6


# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['POST'])
def mine():
    # 1. extracts data from json request
    data = request.get_json()

    # 2. data is a dictionary containing 'proof' and 'id'. Check if they are in data
    if "proof" not in data or "id" not in data:
        response = {"message": "missing proof and id combination"}
        return jsonify(response), 400

    # 3. convert the last block to JSON sorted by its keys
    block_string = json.dumps(blockchain.last_block, sort_keys=True)

    # 4. proof contains the actual proof from the http POST request
    proof = data["proof"]
    recipient_id = data["id"]

    # 5. verify the proof with valid_proof
    if not blockchain.valid_proof(block_string, proof):
        return jsonify({"message": "invalid proof"}), 401

    # 6. the proof of work is valid now get the hash of the last block
    previous_hash = blockchain.hash(blockchain.last_block)

    # 7. forms a block
    block = blockchain.new_block(proof, previous_hash)
    # 8. construct a response to be returned to the client

    # 9. implements a transaction

    blockchain.new_transaction(sender="0", recipient=recipient_id, amount=1)

    response = {
        "message": "New block formed",
        "index": block["index"],
        "transactions": block["transactions"],
        "proof": block["proof"],
        "previous_hash": block["previous_hash"]

    }

    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        # TODO: Return the chain and its current length
        "chain": blockchain.chain,
        "length": len(blockchain.chain)

    }
    return jsonify(response), 200

# return the last block of the chain
@app.route("/last_block", methods=["GET"])
def last_block():

    return jsonify({"last_block": blockchain.last_block}), 200

# create a new transaction end point
@app.route("/transactions/new", methods=["POST"])
def create_new_transaction():

    data = request.get_json()

    if "sender" not in data or "recipient" not in data or "amount" not in data:
        response = {"message": "missing sender, recipient, or amount"}
        return jsonify(response), 400

    index = blockchain.new_transaction(
        data["sender"], data["recipient"], data["amount"])

    response = F"The transaction will be in a block with an index of: {index}"

    return jsonify(response), 201


# Run the program on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
