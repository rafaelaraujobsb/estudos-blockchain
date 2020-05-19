from fastapi import FastAPI

from blockchain import Blockchain


app = FastAPI(title="Conceito Blockchain", version="0.2.0")
blockchain = Blockchain(nivel=5)


@app.get("/minerar-bloco")
def minerar_bloco():
    bloco_anterior = blockchain.get_blobo_anterior()
    proof_anterior = bloco_anterior["proof"]
    proof = blockchain.proof_of_work(proof_anterior)
    hash_anterior = blockchain.hash(bloco_anterior)
    resposta = blockchain.criar_bloco(proof, hash_anterior)
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
