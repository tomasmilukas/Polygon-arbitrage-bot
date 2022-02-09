from web3 import Web3, exceptions
from definedVariables import *

import requests
import os
import json
import config
import time
# import array as arr

matic = config.matic_api
web3 = Web3(Web3.HTTPProvider(matic))

contract_quick_swap = web3.eth.contract(address=quick_router, abi= quick_router_abi)

contract_sushi_swap = web3.eth.contract(address=sushi_router, abi=sushi_router_abi)

number = 1 * 10**18

# number1 = contract_quick_swap.functions.getAmountsOut(number,[wmatic_address, usdc_address]).call()

# number2 = contract_sushi_swap.functions.getAmountsOut(number,[wmatic_address, usdc_address]).call()

# quick_wmatic_price2 = number1[1]/10**6
# sushi_wmatic_price2 = number2[1]/10**6
# print(quick_wmatic_price2, sushi_wmatic_price2)
# print(quick_wmatic_price2 - sushi_wmatic_price2, sushi_wmatic_price2 - quick_wmatic_price2)

# number1 = contract_quick_swap.functions.getAmountsOut(1,[usdc_address, wmatic_address]).call()

# number2 = contract_sushi_swap.functions.getAmountsOut(1,[usdc_address, wmatic_address]).call()

# quick_wmatic_price2 = number1[1]/10**12
# sushi_wmatic_price2 = number2[1]/10**12
# print(quick_wmatic_price2, sushi_wmatic_price2)
# print(quick_wmatic_price2 - sushi_wmatic_price2, sushi_wmatic_price2 - quick_wmatic_price2)


