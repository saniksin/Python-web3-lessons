"""
Отправка транзакции состоит из 3 этапов:
- создание транзакции
- подпись с помощью приватного ключа
- отправка
"""

from network_tbsc_conf import w3 as web3
from account import PK

my_address = web3.to_checksum_address(
    '0x6ea826f099176d56A7b9CbB108aF07a4fb739c7B')
someone_address = web3.to_checksum_address(
    '0x2C43bD7a90cBe1aE7A60F282d7d46d05eFdBde3a')
private_key = PK

"""1. Cоздание транзакции """
from web3 import Web3
def build_txn(
        web3: Web3, 
        from_address: str, 
        to_address: str, 
        amount: float) -> dict[str, int | str]:
    
    # Узнаем цену газа
    gas_price = web3.eth.gas_price

    # Устанавливаем кол-во газа (ставим побольше)
    gas = 2_000_000

    # Число подтверженных транзакций отправителя
    nonce = web3.eth.get_transaction_count(
        web3.to_checksum_address(from_address))

    txn = {
        'chainId': web3.eth.chain_id,
        'from': from_address,
        'to': to_address,
        'value': int(web3.to_wei(amount, 'ether')),
        'nonce': nonce,
        'gasPrice': gas_price,
        'gas': gas
    }
    return txn

transaction = build_txn(
    web3=web3,
    from_address=my_address,
    to_address=someone_address,
    amount=0.1
)

"""2. Подписываем транзакцию приватным ключем """
signed_txn = web3.eth.account.sign_transaction(transaction, private_key)

"""3. Отправка транзакции """
txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

#  Получаем хэш транзакции
print(txn_hash.hex())