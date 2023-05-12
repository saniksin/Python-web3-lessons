"""
Получаем транзакцию по хєшу
1. get_transaction

2. get_transaction_receipt
"""

from network_tbsc_conf import w3 as web3

txn_hash = '0xa4ce41bce2f5e1600a904115e12e11201618e43a25f1f3cee06a675e8791cdb0'
txn_hash2 = '0x760bdbf41eba9b7334a5e686d00c1b112590a971a65b18a1e79cf5d1753cdd50'

# 1. get_transaction
txn = web3.eth.get_transaction(
    web3.to_checksum_address(txn_hash))
print(txn)

# 2. get_transaction_receipt
tnx_receipt = web3.eth.get_transaction_receipt(
    web3.to_checksum_address(txn_hash2))
print(tnx_receipt)