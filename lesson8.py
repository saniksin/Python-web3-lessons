"""
Оценка газа
eth.estimate_gas
"""

from network_tmatic_conf import w3 as web3
from web3.types import TxParams
from typing import cast

user_address = '0x6ea826f099176d56A7b9CbB108aF07a4fb739c7B'

# Формируем транзакцию
amount_of_matic_to_send = 1

txn = {
    'chainId': web3.eth.chain_id,
    'from': user_address,
    'to': user_address,
    'value': int(web3.to_wei(amount_of_matic_to_send, 'ether')),
    'nonce': web3.eth.get_transaction_count(
    web3.to_checksum_address(user_address)),
    'gasPrice': web3.eth.gas_price,
}

# предсказнанное кол-во Wei
gas_value = web3.eth.estimate_gas(cast(TxParams, txn))

# Добавляем 20 процентов на вскидку
gas_value = gas_value / 100 * 120
print(gas_value)