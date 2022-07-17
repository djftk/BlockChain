import hashlib
class Block():
    current_transaction = dict()
    def __init__(self, id, timestamp, data):
        self.new_transaction(data["sender"],data["recipient"],data["amount"])
        self.id = hex(id)
        self.timestamp = timestamp
        self.data = self.current_transaction
        self.previousHash = 0
        self.hash = self.calHash()
    def new_transaction(self, sender, recipient, amount):
        self.current_transaction[hashlib.sha256(hex(len(self.current_transaction)).encode()).hexdigest()[:40]]={'sender' : sender, 'recipient' : recipient, 'amount' : amount}
    def calHash(self):
        return hashlib.sha256(str(self.id).encode()).hexdigest()[:40]