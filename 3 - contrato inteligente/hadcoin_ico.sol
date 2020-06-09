// http://remix.ethereum.org/#appVersion=0.7.7&optimize=false&version=soljson-v0.4.11+commit.68ef5810.js
// https://github.com/MyEtherWallet/etherwallet/releases/tag/v3.11.3.3

// Para rodar o contrato é necessário:
// * Rodar o Ganache
// * Integrar o MyEtherWallet ao Ganache
// * Criar um contrato no MyEtherWallet com o byte code gerado no Remix
// * Pegar somente o que está na chave object
// * Usar uma chave privada de um dos endereços do Ganache
// * Com o contrato inserido na rede, podemos interagir com ele, mas para
// isso precisamos da chave de criação dele e pegar o ABI em MyEtherWallet
// * Ao clicar em Access podemos visualizar todas as funções disponíveis

// versão
pragma solidity ^0.4.11;

contract hadcoin_ico {
    // número máximo de hadcoins disponíveis no ico
    uint public max_hadcoins = 1000000;

    // taxa de cotação de hadcoins para o dolar
    uint public usd_to_hadcoins = 1000;

    // total de hadcoins compradas por investidores
    uint public total_hadcoins_bought = 0;

    // funções de equivalencia
    mapping(address => uint) equity_hadcoins;
    mapping(address => uint) equity_usd;

    // verificando se o investidor pode comprar hadcoins
    modifier can_buy_hadcoins(uint usd_invested) {
        require(usd_invested * usd_to_hadcoins + total_hadcoins_bought <= max_hadcoins);
        _; // significa que a condição tem que ser verdadeira para ser aplicada
    }

    // retorna o valor do investimento em hadcoins
    function equity_in_hadcoins(address investor) external constant returns(uint){
        return equity_hadcoins[investor];
    }

    // retorna o valor do investimento em dolares
    function equity_in_usd(address investor) external constant returns(uint){
        return equity_usd[investor];
    }

    // compra de hadcoins
    function buy_hadcoins(address investor, uint usd_invested) external
    can_buy_hadcoins(usd_invested) {
        uint hadcoins_bought = usd_invested * usd_to_hadcoins;
        equity_hadcoins[investor] += hadcoins_bought;
        equity_usd[investor] = equity_hadcoins[investor] / 1000;
        total_hadcoins_bought += hadcoins_bought;
    }

    // venda de hadcoins
    function sell_hadcoins(address investor, uint hadcoins_sold) external {
        equity_hadcoins[investor] -= hadcoins_sold;
        equity_usd[investor] = equity_hadcoins[investor] / 1000;
        total_hadcoins_bought -= hadcoins_sold;
    }
}