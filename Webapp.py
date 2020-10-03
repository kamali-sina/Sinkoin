"""
Created on Sat Oct 3 13:47:22 2020

@author: TUS
"""
from uuid import uuid4
from flask import Flask, jsonify, request
from Sinkoin import Sinkoin, COINS_REWARDED_PER_MINE
import json

web_app = Flask('Sinkoin Blockchain Webapp') 
blockchain = Sinkoin()

node_address = ""


@web_app.route('/', methods=['GET'])
def welcome_user():
    response = 'hello bro! enjoy blockchains!'
    return response, 200


@web_app.route('/mine_block', methods=['GET'])
def mine_block():
    last_block = blockchain.get_last_block()
    previous_proof = last_block['proof']
    proof = blockchain.find_proof_of_work(previous_proof)
    blockchain.add_transaction('blockchain_base',node_address, COINS_REWARDED_PER_MINE)
    new_block = blockchain.create_block(proof, blockchain.hash_block(last_block))
    response = {'message': 'Congrats! You mined a block!'}
    response.update(new_block)
    return jsonify(response), 200


@web_app.route('/chain', methods=['GET'])
def get_chain():
    response = {'chain':blockchain.chain, 
                'lenght': len(blockchain.chain)}
    return jsonify(response), 200


@web_app.route('/is_valid', methods=['GET'])
def get_validity():
    response = {'message': str(blockchain.is_chain_valid(blockchain.chain))}
    return jsonify(response), 200


@web_app.route('/add_transaction', methods=['POST'])
def add_transaction():
    json = request.get_json()
    transaction_keys = ['sender','reciever','amount']
    if not all (key in json for key in transaction_keys):
        response = {'message': 'Some elements are missing!'}
        return jsonify(response), 400
    blockchain.add_transaction(json['sender'], json['reciever'], json['amount'])
    response = {'message': 'Transaction has been successfully added to mempool.'}
    return jsonify(response), 201


web_app.run(host='0.0.0.0', port=5000)