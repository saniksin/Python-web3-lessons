"""
Multicall
https://github.com/shamaevnn/awesome-contract-addresses#multicall-addresses
allowance к разным контрактам
"""

from dataclasses import dataclass
from typing import Dict, List, cast
from eth_utils.hexadecimal import encode_hex, add_0x_prefix
from web3._utils.contracts import encode_abi
from eth_utils.abi import function_abi_to_4byte_selector
from web3._utils.abi import get_abi_output_types
from web3 import Web3 
from web3.types import ABIFunction
from hexbytes import HexBytes

rpc_url = 'https://mainnet.optimism.io'
web3 = Web3(Web3.HTTPProvider(rpc_url))

# Определение класса для хранения информации о контракте и адресе токена
@dataclass
class ApproveAddressesInfo:
    approval_address: str # контракт, которому дали approve
    token_address: str # адрес токена

    def __hash__(self):
        return hash((self.approval_address, self.token_address))

    def __eq__(self, other):
        if not isinstance(other, ApproveAddressesInfo):
            return False
        return (
            self.approval_address == other.approval_address
            and self.token_address == other.token_address
        )

encode_hex_fn_abi = lambda fn_abi: encode_hex(
    function_abi_to_4byte_selector(fn_abi)
)

# можно подсмотреть в ABI ERC-20 
ALLOWANCE_ABI = {"constant": True, "inputs": [{"internalType": "address", "name": "owner", "type": "address"}, {"internalType": "address", "name": "spender", "type": "address"}], "name": "allowance", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "payable": False, "stateMutability": "view", "type": "function"}
allowance_selector = encode_hex_fn_abi(ALLOWANCE_ABI)
# а это в ABI multicall контрактов
TRY_AGGREGATE_ABI: ABIFunction = {"inputs":[{"name":"requireSuccess","type":"bool"},{"components":[{"name":"target","type":"address"},{"name":"callData","type":"bytes"}],"name":"calls","type":"tuple[]"}],"name":"tryAggregate","outputs":[{"components":[{"name":"success","type":"bool"},{"name":"returnData","type":"bytes"}],"name":"returnData","type":"tuple[]"}],"stateMutability":"nonpayable","type":"function"}
try_aggregate_selector = encode_hex_fn_abi(TRY_AGGREGATE_ABI)
try_aggregate_output_types = get_abi_output_types(TRY_AGGREGATE_ABI)


# Функция для вызова функции `multicall_check_allowance`
def multicall_cheсk_allowance(
        web3: Web3,
        multicall_address: str,
        user_address: str,
        approval_token_addresses: List[ApproveAddressesInfo],
) -> Dict[ApproveAddressesInfo, str]:
    
    # Закодирование данных функции `allowance` для каждого контракта
    encoded = (
    (
        addresses.token_address,
        encode_abi(
            web3,
            cast(ABIFunction, ALLOWANCE_ABI),
            # адрес пользователя и адрес контракта на approve
            arguments=(user_address, addresses.approval_address),
            data=allowance_selector,
        ),
    )
    for addresses in approval_token_addresses
)
    
    # Закодирование данных функции `tryAggregate` для мультиколла
    data = add_0x_prefix(
        encode_abi(
            web3,
            TRY_AGGREGATE_ABI,
            (False, [(token_addr, enc) for token_addr, enc in encoded]),
            try_aggregate_selector,
        )
    )

    # Вызов метода `call` для мультиколла
    tx_raw_data = web3.eth.call({
        "to": multicall_address,
        "data": data,
    })

    # Декодирование сырых данных транзакции и извлечение результатов
    output_data = web3.codec.decode(
        try_aggregate_output_types, tx_raw_data)[0]
    output_data = (
        str(web3.codec.decode(["uint256"], HexBytes(raw_token_address))[0]) \
        for (_, raw_token_address) in output_data
    )

    # Создание словаря, связывающего информацию о контрактах с результатами
    return dict(zip(approval_token_addresses, output_data))


# Пример вызова функции
multicall_address = '0xcA11bde05977b3631167028862bE2a173976CA11'
user_address = '0x6ea826f099176d56A7b9CbB108aF07a4fb739c7B'
result = multicall_cheсk_allowance(
    web3,
    multicall_address,
    user_address,
    approval_token_addresses=[
        ApproveAddressesInfo(
            approval_address='0x000000000022D473030F116dDEE9F6B43aC78BA3',
            token_address='0x4200000000000000000000000000000000000042', # OP token
        ),
        ApproveAddressesInfo(
            approval_address='0x794a61358D6845594F94dc1DB02A252b5b4814aD',
            token_address='0x7F5c764cBc14f9669B88837ca1490cCa17c31607', # USDC token
        ),
        ApproveAddressesInfo(
            approval_address='0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45',
            token_address='0x94b008aA00579c1307B0EF2c499aD98a8ce58e58', # USDT token
        )
    ]
)

print(result)