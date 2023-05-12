"""
PRC connect/gas price/check wallet balance/
"""

from web3 import Web3

# подключение к сети
rpc_url = "https://data-seed-prebsc-1-s1.binance.org:8545/"
w3 = Web3(Web3.HTTPProvider(rpc_url))
print(f"Is conneted: {w3.is_connected()}")

# проверка цены газа
gas_price_now = w3.eth.gas_price/1_000_000_000_000_000_000
formatted_gas_price = '{:.8f}'.format(gas_price_now)
print(f"gas price: {(formatted_gas_price)}") # кол-во Wei за единицу газа

# текущий блок
print(f"current block number: {w3.eth.block_number}")

# сhain id
print(f"number of current chain is {w3.eth.chain_id}")

# смотрим баланс кошелька (по стандарту отображает в Wei)
wallet_address = "0x6ea826f099176d56A7b9CbB108aF07a4fb739c7B"
checksum_address = Web3.to_checksum_address(wallet_address)
balance = w3.eth.get_balance(checksum_address)
print(f"balance of {wallet_address}={balance} Wei")

# переводим баланс в привычный формат
ether_balance = Web3.from_wei(balance, 'ether') # Decimal ('1')
gwei_balance = Web3.from_wei(balance, 'gwei') # Decimal('1000000000')
wei_balance = Web3.to_wei(ether_balance, 'ether') # 1000000000000000000
print(ether_balance)
