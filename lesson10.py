"""
Баланс нескольких токенов за один запрос 
BalanceScanner
tokensBalance — узнать баланс нескольких токенов для юзера;
"""

from eth_utils.hexadecimal import encode_hex, add_0x_prefix
from web3._utils.contracts import encode_abi
from eth_utils.abi import function_abi_to_4byte_selector
from web3._utils.abi import get_abi_output_types
from web3 import Web3 
from hexbytes import HexBytes
from typing import cast
from web3.types import ABIFunction, TxParams

# инициализация 
web3 = Web3(Web3.HTTPProvider("https://bsc-dataseed1.defibit.io"))

# ABI функции tokensBalance. 
TOKENS_BALANCE_ABI = {
    "inputs": [
        {
            "internalType": "address",
            "name": "owner",
            "type": "address"
        },
        {
            "internalType": "address[]",
            "name": "contracts",
            "type": "address[]"
        }
    ],
    "name": "tokensBalance",
    "outputs": [
        {
            "components": [
                {
                    "internalType": "bool",
                    "name": "success",
                    "type": "bool"
                },
                {
                    "internalType": "bytes",
                    "name": "data",
                    "type": "bytes"
                }
            ],
            "internalType": "struct BalanceScanner.Result[]",
            "name": "results",
            "type": "tuple[]"
        }
    ],
    "stateMutability": "view",
    "type": "function"
}
TOKENS_BALANCE_SELECTOR = encode_hex(
    function_abi_to_4byte_selector(TOKENS_BALANCE_ABI))
tokens_balance_output_types = get_abi_output_types(
    cast(ABIFunction, TOKENS_BALANCE_ABI))

# баланс каких токенов будем проверять
tokens_to_check = [
    '0x55d398326f99059fF775485246999027B3197955', # USDT
    '0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d', # USDC
    '0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56', # BUSD
]

# адрес пользователя, для которого будем смотреть баланс
user_address = "0x6ea826f099176d56A7b9CbB108aF07a4fb739c7B"

encoded_data = encode_abi(
    w3=web3,
    abi=cast(ABIFunction, TOKENS_BALANCE_ABI),
    arguments=(user_address, [t for t in tokens_to_check]),  # аргументы функции tokensBalance
    data=TOKENS_BALANCE_SELECTOR,
)

tx = {
    # (https://github.com/shamaevnn/awesome-contract-addresses#balancescanner)
    "to": "0x83cb147c13cBA4Ba4a5228BfDE42c88c8F6881F6",  # адрес контракта BalanceScanner 
    "data": encoded_data
}

# обращаемся к ноде
tx_raw_data = web3.eth.call(cast(TxParams, tx))
output_data = web3.codec.decode(tokens_balance_output_types, tx_raw_data)[0]
res = {}
for token_address, (_, bytes_balance) in zip(tokens_to_check, output_data):
    wei_balance = web3.codec.decode(["uint256"], HexBytes(bytes_balance))[0]
    res[token_address] = wei_balance

print(res)