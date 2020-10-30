"""
Created on Sat Oct 3 13:47:22 2020

@author: TUS
"""
import datetime
import hashlib

class Block:
    """Currently not used because can't jsonify this object"""
    def __init__(self, proof, index, transactions, previous_hash):
        self.index = index
        self.timestamp = int(datetime.datetime.now().timestamp())
        self.proof = proof
        self.transactions = transactions
        self.previous_hash = previous_hash

    def hash(self):
        encoded_block = json.dumps(self.to_dict(), sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def to_dict(self):
        datetime_obj = datetime.datetime.fromtimestamp(self.timestamp)
        return {'index': self.index,
                'timestamp': str(datetime_obj),
                'proof': self.proof,
                'transactions': self.transactions,
                'previous_hash': self.previous_hash}
    
    def __str__(self):
        datetime_obj = datetime.datetime.fromtimestamp(self.timestamp)
        return str({'index': self.index,
                'timestamp': str(datetime_obj),
                'proof': self.proof,
                'transactions': self.transactions,
                'previous_hash': self.previous_hash})