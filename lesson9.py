"""
Ускоряем инициализацию контрактов
"""

# Cтарый способ проверки баланса lesson4

from network_tbsc_conf import w3 as web3, \
            ERC20_ABI, usdt_contract_address

def get_balance_old(web3, token_address, user_address):
    # инициализация контракта
    token_contract = web3.eth.contract(token_address, abi=ERC20_ABI)

    # получение данных из ноды
    balance = token_contract.functions.balanceOf(user_address).call()
    return int(balance)


# Убираем лишнее и оставляем только balanceOf
import json
from web3.types import ABIFunction
from eth_utils.hexadecimal import encode_hex, add_0x_prefix
from eth_utils.abi import function_abi_to_4byte_selector
from web3._utils.contracts import encode_abi
from web3._utils.abi import get_abi_output_types

encode_hex_fn_abi = lambda fn_abi: encode_hex(
    function_abi_to_4byte_selector(fn_abi)
)

# словарь с функцией balanceOf и decimal
BALANCE_OF_ABI: ABIFunction = json.loads('{"constant":true,"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}')
DECIMAL_ABI = json.loads('{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"}')

balance_of_selector = encode_hex_fn_abi(BALANCE_OF_ABI)
decimals_selector = encode_hex_fn_abi(DECIMAL_ABI)

balance_of_output_types = get_abi_output_types(BALANCE_OF_ABI)
decimals_output_types = get_abi_output_types(DECIMAL_ABI)

def get_balance_new(web3, user_address, token_address):
    # инициализация контракта
    balance_data = add_0x_prefix(encode_abi(
        web3,
        abi=BALANCE_OF_ABI,
        arguments=(user_address,), # аргумент функции balanceOf
        data = balance_of_selector,
        ),
    )

    decimal_data = add_0x_prefix(encode_abi(
        web3, 
        abi=DECIMAL_ABI, 
        arguments=[],
        data=decimals_selector,
        ),
    )

    balance_tx = {"to": token_address, "data": balance_data}
    decimals_tx = {"to": token_address, "data": decimal_data}

    # получение данных из ноды
    balance_res = web3.eth.call(balance_tx)
    decimal_res = web3.eth.call(decimals_tx)

    balance_output_data = web3.codec.decode(
        balance_of_output_types, balance_res)
    decimal_output_data = web3.codec.decode(
        decimals_output_types, decimal_res)

    balance = balance_output_data[0]
    decimals = decimal_output_data[0]
    
    token_balance = balance / (10 ** decimals)
    return token_balance


user_address = '0x6ea826f099176d56A7b9CbB108aF07a4fb739c7B'
# balance wei
balance = get_balance_new(web3=web3, user_address=user_address, token_address=usdt_contract_address)
print(balance)