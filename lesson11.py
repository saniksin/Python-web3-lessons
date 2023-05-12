"""
Баланс нескольких токенов за один запрос 
BalanceScanner
tokenBalances — узнать баланс нескольких юзеров для токена.
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

# ABI функции tokenBalances.
TOKEN_BALANCES_ABI = {
    "inputs": [
        {"internalType": "address[]", "name": "addresses", "type": "address[]"},
        {"internalType": "address", "name": "token", "type": "address"}
    ],
    "name": "tokenBalances",
    "outputs": [
        {
            "components": [
                {"internalType": "bool", "name": "success", "type": "bool"},
                {"internalType": "bytes", "name": "data", "type": "bytes"}
            ],
            "internalType": "struct BalanceScanner.Result[]",
            "name": "results",
            "type": "tuple[]"
        }
    ],
    "stateMutability": "view",
    "type": "function"
}
TOKEN_BALANCES_SELECTOR = encode_hex(
    function_abi_to_4byte_selector(TOKEN_BALANCES_ABI))
token_balances_output_types = get_abi_output_types(
    cast(ABIFunction, TOKEN_BALANCES_ABI))

# баланс каких токенов будем проверять
wallets_to_check = [
    '0x6ea826f099176d56A7b9CbB108aF07a4fb739c7B',
    '0x2C43bD7a90cBe1aE7A60F282d7d46d05eFdBde3a',
]

# адрес контракта пользователя, для которого будем смотреть баланс
token_address = '0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56' # BUSD
encoded_data = encode_abi(
    w3=web3,
    abi=cast(ABIFunction, TOKEN_BALANCES_ABI),
    arguments=([w for w in wallets_to_check], token_address),
    data=TOKEN_BALANCES_SELECTOR,
)

tx = {
    # (https://github.com/shamaevnn/awesome-contract-addresses#balancescanner)
    "to": "0x83cb147c13cBA4Ba4a5228BfDE42c88c8F6881F6",  # адрес контракта BalanceScanner
    "data": encoded_data
}

# обращаемся к ноде
tx_raw_data = web3.eth.call(cast(TxParams, tx))
output_data = web3.codec.decode(token_balances_output_types, tx_raw_data)[0]
res = {}
for token_address,(_, bytes_balance) in zip(wallets_to_check, output_data):
    wei_balance = web3.codec.decode(["uint256"], HexBytes(bytes_balance))[0]
    res[token_address] = wei_balance

print(res)