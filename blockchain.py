import hashlib
import time
import json
import ast

class Block():
    current_transaction = dict()#거래내역 선언
    def __init__(self, id, timestamp, data):
        self.new_transaction(data["sender"],data["recipient"],data["amount"])
        self.id = hex(id)
        self.timestamp = timestamp
        self.data = self.current_transaction
        self.previousHash = 0
        self.hash = self.calHash()
    def new_transaction(self, sender, recipient, amount):
        # 거래 내역을 current_transaction에 추가 합니다. 현재 거래내역의 숫자를 이용하여 sha256해시함수를 적용합니다. 내용은 보내는사람, 받는사람, 금액, 이전 거래내역 해시키입니다.
        self.current_transaction[hashlib.sha256(hex(len(self.current_transaction)).encode()).hexdigest()[:40]]={'sender' : sender, 'recipient' : recipient, 'amount' : amount, 'previoustransaction':hashlib.sha256(hex(len(self.current_transaction)-1).encode()).hexdigest()[:40]}
    def calHash(self):
        #블록의 해시키를 설정합니다.
        return hashlib.sha256(str(self.id).encode() + str(self.data).encode() + str(self.timestamp).encode() + str(self.previousHash).encode()).hexdigest()[:40]

class BlockChain:

    def __init__(self):
        #블록을 저장할 리스트를 설정합니다.
        self.chain = []
        self.createGenesis()

        #초기 블록을 생성합니다.
    def createGenesis(self):
        self.chain.append(Block(0, time.time(),  {"sender":"h1","amount":5,"recipient":"h2"}))

        #새로운 블록을 블록체인 리스트에 넣어줍니다.
    def addBlock(self, nBlock):
        #블록체인 증명을 위해서 입증 이전 블록의 해시값을 현재 블록의 previousHash키에 넣어줍니다.
        nBlock.previousHash = self.chain[len(self.chain)-1].hash
        nBlock.hash = nBlock.calHash()
        self.chain.append(nBlock)

    def last_block(self):
        # 블록체인 리스트에 가장 마지막 블록을 돌려줍니다.
        return self.chain[-1]

        #블록체인 리스트의 유효성을 증명합니다.
    def isValid(self):
        i = 1
        while(i<len(self.chain)):
            #블록체인 리스트의 블록의 해시값이 옳바르게 설정되어 있는지 확입합니다.
            if(self.chain[i].hash != self.chain[i].calHash()):
                return False
            #블록체인 리스트의 이전 블록의 해시값과 현재 블록이 저장하고 있는 previousHash값이 일치하는지 확인합니다.
            if(self.chain[i].previousHash != self.chain[i-1].hash):
                return False
            #블록체인 리스트의 존재하는 모든 블록을 검사합니다.
            i += 1
        return True

        #거래내역의 유효성겁사
    def istransactionValid(self):
        i=1
        while(i<len(self.chain[0].data)):
            #print(hashlib.sha256(hex(i-1).encode()).hexdigest()[:40])
            #print(self.chain[i].data[hashlib.sha256(hex(i).encode()).hexdigest()[:40]]["previoustransaction"])
            #블록체인 리스트의 블록 거래내역(data)가 가지고 있는 이전 거래내역 값이 거래내역의 해시함수 키와 일치하는지 검사합니다.
            if(hashlib.sha256(hex(i-1).encode()).hexdigest()[:40] != self.chain[i].data[hashlib.sha256(hex(i).encode()).hexdigest()[:40]]["previoustransaction"]):
                return False
            i+=1
        return True

        #블록을 채굴하기 위한 proof값을 돌려줍니다.
    def pow(self, last_proof):
        proof = 0
        #print(last_proof)
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

        #블록의 해시값 4자리수가 특정숫자와 만나서 0000이 된다면 그 숫자가 블록을 캘수 있는 키값입니다. 나중에 검증에 사용할 수 있을 것 같아 구현해보았습니다.
    @staticmethod
    def valid_proof(last_proof, proof):
        guess = str(last_proof + str(proof)).encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000" # nonce​

start = time.time() #시간 측정
newblockchain = BlockChain() #블록체인 객체 생성
print(json.dumps(vars(newblockchain.chain[0]), indent=4))#블록체인 출력
#블록체인에 새로운 블록 추가
newblockchain.addBlock(Block(len(newblockchain.chain),time.time(), {"sender":"h1","amount":4,"recipient":"h2"}))
for block in newblockchain.chain:
    print(json.dumps(vars(block), indent=4))
end = time.time() #시간 측정

last_block = newblockchain.last_block()
print("-------------------------------")
last_block=json.dumps(vars(last_block))#블록체인의 마지막 블록 가져오기
my_dict = ast.literal_eval(last_block)#블록체인을 사전형태로 고정
#print(my_dict)
#print(my_dict['hash'])
last_hash = my_dict['hash']
proof = newblockchain.pow(last_hash)#블록체인의 마지막 블록 해시값으로 키값 받아오기
print(proof)
print("===========================================")
print(newblockchain.istransactionValid())#블록체인 거래내역 증명
print(f"{end - start:.5f} sec")#완료시간 출력
