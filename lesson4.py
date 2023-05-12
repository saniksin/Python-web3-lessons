"""
Смарт контракты
ERC-20 токены
ABI
Read operation
"""

import json
from network_tbsc_conf import w3 as web3


# одинаковый для всех ERC20 токенов ABI
ERC20_ABI = json.loads('''[{"inputs":[{"internalType":"string","name":"_name","type":"string"},{"internalType":"string","name":"_symbol","type":"string"},{"internalType":"uint256","name":"_initialSupply","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint8","name":"decimals_","type":"uint8"}],"name":"setupDecimals","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]''')

usdt_contract_address = web3.to_checksum_address('0xA11c8D9DC9b66E209Ef60F0C8D969D3CD988782c')

# инициализация USDT контракта
usdt_contract = web3.eth.contract(usdt_contract_address, abi=ERC20_ABI)

# просмотр всех возможных функций
all_function = usdt_contract.all_functions()
print(f"все функции ERC20 токена: \n{all_function}")


user_address = '0x6ea826f099176d56A7b9CbB108aF07a4fb739c7B'
some_contract_address = '0x9a489505a00cE272eAa5e07Dba6491314CaE3796'

# Read functions
token_name = usdt_contract.functions.name().call() # Имя токена
print(token_name)

balance_of_token = usdt_contract.functions.balanceOf(
    user_address).call() # balance in Wei
print(balance_of_token)

token_symbol = usdt_contract.functions.symbol().call() # символ токена
print(token_symbol) 

token_decimals = usdt_contract.functions.decimals().call() # дробность токена
print(token_decimals) 

allowance = usdt_contract.functions.allowance(
    user_address, some_contract_address).call() # Разрешенное использование токенов другим контрактом/адресом.

# Выводим информацию которую обработали выше 
ether_balance = balance_of_token / 10 ** token_decimals
print(f'Balance of {token_name}({token_symbol}) is {ether_balance}')
print(f'Allowance for {some_contract_address} is {allowance}')
