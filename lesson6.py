"""
Write contract
-- allowance --
"""

from network_tbsc_conf import w3 as web3, usdt_contract
from web3.types import TxParams
from account import PK


user_address = '0x6ea826f099176d56A7b9CbB108aF07a4fb739c7B'
some_contract_address = '0x9a489505a00cE272eAa5e07Dba6491314CaE3796'

dict_transaction: TxParams = {
    'chainId': web3.eth.chain_id,
    'gas': 210000,
    'gasPrice': web3.eth.gas_price,
    'nonce': web3.eth.get_transaction_count(
    web3.to_checksum_address(user_address)),
}

# даем разрешение на использование максимального кол-ва токенов
approve_amount = 2 ** 256 - 1 

# создаем транзакцию
transaction = usdt_contract.functions.approve(
    some_contract_address, approve_amount
).build_transaction(dict_transaction)

# Подписываем 
signed_txn = web3.eth.account.sign_transaction(
    transaction, PK
)

# Отправляем транзацию и проверяем
txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
print(txn_hash.hex())