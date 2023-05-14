"""
Асинхронность
"""

import time
import asyncio
from web3 import Web3
from web3.eth.async_eth import AsyncEth
from typing import Dict, List

rpc_url_by_chain_id = {
    1: "https://eth.llamarpc.com", #ETH
    56: "https://bsc-dataseed3.ninicoin.io", # BSC
    137: "https://rpc-mainnet.matic.quiknode.pro", # Polygon
    250: "https://rpc.fantom.network",  # Fantom
    43114: "https://rpc.ankr.com/avalanche", # Avalanche
    42161: "https://rpc.ankr.com/arbitrum", # Arbitrum
    10: "https://mainnet.optimism.io", # Optimism
}


# инициализация СИНХРОННОЙ версии web3 для каждой сети 
sync_web3_by_chain_id = {}
for chain_id, rpc_url in rpc_url_by_chain_id.items():
    sync_web3_by_chain_id[chain_id] = Web3(Web3.HTTPProvider(rpc_url))

# Инициализация АСИНХРОННОЙ версии web3 для каждой сети
async_web3_by_chain_id = {}
for chain_id, rpc_url in rpc_url_by_chain_id.items():
    async_web3 = Web3(
        Web3.AsyncHTTPProvider(rpc_url), 
        modules={"eth": (AsyncEth,)}, middlewares=[]
    )
    async_web3_by_chain_id[chain_id] = async_web3

def get_sync(chain_ids: List[int]) -> Dict[int, float]:
    """
    chain_ids = [1, 56, 137, 250, 43114, 42161, 10]
    -> {1: '0.0001 ETH', 56: '0.0002 ETH', ...}
    """

    res, start_time = {}, time.time()
    for chain_id in chain_ids:
        web3 = sync_web3_by_chain_id[chain_id]
        res[chain_id] = web3.eth.gas_price
    print(f"{(time.time()-start_time):.3f} секунд для СИНХРОННОЙ ВЕРСИИ")
    return res


async def get_async(chain_ids: List[int]) -> Dict[int, float]:
    """
    chain_ids = [1, 56, 137, 250, 43114, 42161, 10]
    -> {1: '0.0001 ETH', 56: '0.0002 ETH', ...}
    """
    
    tasks, res, start_time = [], {}, time.time()
    for chain_id in chain_ids:
        async_web3 = async_web3_by_chain_id[chain_id] 
        tasks.append(async_web3.eth.gas_price) # добавляем асинхронные задачи
    gas_price = await asyncio.gather(*tasks) # запускаем сразу несколько задач
    print(f"{(time.time()-start_time):.3f} секунд для АСИНХРОННОЙ ВЕРСИИ")
    return dict(zip(chain_ids, gas_price))


if __name__ == "__main__":
    print(get_sync([1, 56, 137, 250, 43114, 42161, 10]))
    print(asyncio.run(get_async([1, 56, 137, 250, 43114, 42161, 10])))