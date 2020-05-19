import json
import hashlib
from datetime import datetime


class Blockchain:
    def __init__(self, nivel: int = 4):
        self.chain = []
        self.__dificuldade = nivel
        self.criar_bloco(proof=1, hash_anterior='0')
    
    def criar_bloco(self, proof: int, hash_anterior: str) -> dict:
        bloco = {
            "index": len(self.chain) + 1,
            "timestamp": str(datetime.now()),
            "proof": proof,
            "hash_anterior": hash_anterior
        }
        self.chain.append(bloco)

        return bloco

    def get_blobo_anterior(self):
        return self.chain[-1]

    def __operacao_hash(self, novo_proof: int, proof_anterior: int) -> str:
        return hashlib.sha256(str(novo_proof**2 - proof_anterior**2).encode()).hexdigest()

    def __is_operacao_valida(self, hash256: str) -> bool:
        return hash256[:self.__dificuldade] == "0"*self.__dificuldade

    def proof_of_work(self, proof_anterior: int) -> int:
        novo_proof = 1

        while self.__is_operacao_valida(self.__operacao_hash(novo_proof, proof_anterior)) is False:
            novo_proof += 1

        return novo_proof

    def hash(self, bloco: dict) -> str:
        return hashlib.sha256(json.dumps(bloco, sort_keys=True).encode()).hexdigest()

    def is_chain_valida(self, chain: list) -> bool:
        resposta = True
        index_bloco = 1
        bloco_anterior = chain[0]

        while index_bloco < len(chain):
            bloco = chain[index_bloco]
            if bloco["hash_anterior"] != self.hash(bloco_anterior):
                resposta = False
            else:
                proof_anterior, proof = bloco_anterior["proof"], bloco["proof"]
                if self.__is_operacao_valida(self.__operacao_hash(proof, proof_anterior)):
                    bloco_anterior = bloco
                    index_bloco += 1
                else:
                    resposta = False

        return resposta