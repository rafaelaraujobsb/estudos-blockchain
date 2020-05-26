from uuid import uuid4
from copy import deepcopy

from fastapi import FastAPI

from hadcoin import Blockchain


app = FastAPI(title="Conceito Blockchain", version="0.2.0")
blockchain = Blockchain(nivel=5)
endereco_no = str(uuid4()).replace("-", "")


@app.get("/minerar-bloco")
def minerar_bloco():
    bloco_anterior = blockchain.get_blobo_anterior()
    proof_anterior = bloco_anterior["proof"]
    proof = blockchain.proof_of_work(proof_anterior)
    hash_anterior = blockchain.hash(bloco_anterior)
    blockchain.adicionar_transacao(endereco_no, destinatario="Rafael", valor=1)
    resposta = deepcopy(blockchain.criar_bloco(proof, hash_anterior))
    resposta["mensagem"] = "Você acabou de minerar um bloco!"

    return resposta


@app.get("/chain")
def chain():
    resposta = {
        "chain": blockchain.chain,
        "tamanho": len(blockchain.chain)
    }

    return resposta


@app.get("/validar")
def validar():
    if blockchain.is_chain_valida(blockchain.chain):
        resposta = {"mensagem": "Blockchain válida!"}
    else:
        resposta = {"mensagem": "Blockchain inválida"}

    return resposta


@app.post("/adicionar-transacao")
def adicionar_transacao(json: dict):
    chaves_transacao = ["remetente", "destinatario", "valor"]
    if all(chave in chaves_transacao for chave in json.keys()):
        index = blockchain.adicionar_transacao(**json)
        resposta = {"mensagem": f"Essa transação foi adicionada ao bloco {index}"}
    else:
        resposta = {"mensagem": "Alguns elementos estão faltando"}

    return resposta


@app.post("/conectar-no")
def conectar_no(json: dict):
    nos = json.get("nos")
    if nos is None:
        resposta = {"mensagem": "Alguns elementos estão faltando"}
    else:
        for no in nos:
            blockchain.adicionar_no(no)
        resposta = {"mensagem": f"Os nós foram conectados!", "total_nos": list(blockchain.nos)}

    return resposta


@app.get("/substituir-chain")
def substituir_chain():
    if blockchain.substituir_chain():
        resposta = {"mensagem": "Chain alterada!"}
    else:
        resposta = {"mensagem": "Chain não foi alterada!"}

    resposta["chain"] = blockchain.chain

    return resposta
