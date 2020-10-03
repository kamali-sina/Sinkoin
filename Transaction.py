"""
Created on Sat Oct 3 13:47:22 2020

@author: TUS
"""
class Transaction(object):
    """Currently not used because can't jsonify this object"""
    def __init__(self, sender, reciever, amount):
        self.sender = sender
        self.reciever = reciever
        self.amount = amount
    
    def to_dict(self):
        return {'sender': self.sender,
                'reciever': self.reciever,
                'amount': self.amount}
    
    def __str__(self):
        return str({'sender': self.sender,
                    'reciever': self.reciever,
                    'amount': self.amount})