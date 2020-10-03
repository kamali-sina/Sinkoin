# -*- coding: utf-8 -*-
"""
Created on Sat Oct 3 13:47:22 2020

@author: TUS
"""
import datetime
import hashlib
from flask import Flask, jsonify, request
import requests
from uuid import uuid4
from urllib.parse import urlparse

LEADING_ZEROES = 4
COINS_REWARDED_PER_MINE = 50

#TODO: add public keys and private keys use randoms and eliptic curve cryptography. add signing transactions and the function that checks this.
#TODO: add '/get_random_private_key' to the web app. make mining a real shit. make blockchains update.
class Sinkoin:
    """
    This object stores a single chain from the block chain.
    """
    def __init__(self):
        self.chain = []
        self.mempool = []
        # genesis block
        self.create_block(proof=1, previous_hash='0')
        self.nodes = set()

    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1,
                'timestamp': int(datetime.datetime.now().timestamp()),
                'proof': proof,
                'transactions': self.mempool,
                'previous_hash': previous_hash}
        self.mempool = []
        self.chain.append(block)
        return block

    def get_last_block(self):
        return self.chain[-1]

    def find_proof_of_work(self, previous_proof):
        new_proof = 1
        while (True):
            hasher = self.get_proof_hash(new_proof, previous_proof)
            if (hasher[:LEADING_ZEROES] == LEADING_ZEROES * '0'):
                break
            new_proof += 1
        return new_proof

    def hash_block(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def get_proof_hash(self, proof, previous_proof):
        hashed_proof = hashlib.sha256(str(proof**2 - previous_proof**2).encode())
        return hashed_proof.hexdigest()

    def is_chain_valid(self, chain):
        for i in range(1, len(chain)):
            block = chain[i]
            previous_block = chain[i-1]
            if (block['previous_hash'] != self.hash_block(previous_block)):
                return False
            if (self.get_proof_hash(block['proof'], previous_block['proof'])[:LEADING_ZEROES] != LEADING_ZEROES*'0'):
                return False
        return True
    
    def add_transaction(self, sender, reciever, amount):
        self.mempool.append({'sender': sender,
                            'reciever': reciever,
                            'amount': amount})
        return self.get_last_block()['index'] + 1

    def add_node(self, address):
        parsed_node = urlparse(address)
        self.nodes.add(parsed_node.netloc)
    
    def update_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f"http://{node}/get_chain")
            if response.status_code == 200:
                lenght = response.json()['lenght']
                chain = response.json()['chain']
                if ((lenght > max_length) and (self.is_chain_valid(chain))):
                    longest_chain = chain
                    max_length = lengh
        if (longest_chain):
            return True
            self.chain = chain
        return False
