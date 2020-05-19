import json
import hashlib
from uuid import uuid4
from datetime import datetime
from urllib.parse import urlparse

import requests


class Blockchain:
    def __init__(self, nivel: int = 4):
        self.chain = []
        self.nos = set()
        self.transacoes = []
        self.__dificuldade = nivel
        self.criar_bloco(proof=1, hash_anterior='0')

    def adicionar_transacao(self, remetente: str, destinatario: str, valor: float)
        self.transacoes.append({"remetente": remetente, "destinatario": destinatario, "valor": valor})
        return self.get_blobo_anterior()["index"] + 1

    def adicionar_no(self, endereco: str):
        url_parse = urlparse(endereco)
        self.nos.add(url_parse.netloc)

    def substituir_chain(self):
        network = self.nos
        maior_chain = None
        tamanho_maximo = len(self.chain)
        
        for no in network:
            resposta = requests.get(f"http://{no}/chain")

            if resposta.status_code == 200:
                chain = resposta.json()["chain"]
                tamanho = resposta.json()["tamanho"]

                if tamanho > tamanho_maximo and self.is_chain_valida(chain):
                    maior_chain = chain
                    tamanho_maximo = tamanho

        if maior_chain:
            self.chain = chain
            resposta = True
        else:
            resposta = False

        return resposta

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
