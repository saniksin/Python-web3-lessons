"""
Write contract
-- send transaction --
"""

from network_tbsc_conf import w3 as web3, usdt_contract
from account import PK
from typing import cast
from web3.types import TxParams

user_address = '0x6ea826f099176d56A7b9CbB108aF07a4fb739c7B'
someone_address = '0x2C43bD7a90cBe1aE7A60F282d7d46d05eFdBde3a'

dict_transaction = { 
    'chainId': web3.eth.chain_id,
    'from': user_address,
    'gasPrice': web3.eth.gas_price,
    'nonce': web3.eth.get_transaction_count(
    web3.to_checksum_address(user_address)),
}

# вычисляем 1 USDT
usdt_decimals = usdt_contract.functions.decimals().call()
one_usdt = 1 * 10 ** usdt_decimals 

# cоздаем транзакцию на 100 USDT
transaction = usdt_contract.functions.transfer(
    someone_address, one_usdt*100
).build_transaction(cast(TxParams, dict_transaction))

# подписываем транзакцию
signed_txn = web3.eth.account.sign_transaction(
    transaction, PK)

tnx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
print(tnx_hash.hex())

