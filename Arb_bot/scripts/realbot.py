from web3 import Web3, exceptions
from definedVariables import *

import requests
import os
import json
import config
import time

# create config file, put in variables and run this again.

matic = os.environ.get('matic_api')
web3 = Web3(Web3.HTTPProvider(matic))
starttime = time.time()

# Contract definitions

contract_quick_swap = web3.eth.contract(address=quick_router, abi= quick_router_abi)

contract_ape_swap = web3.eth.contract(address=ape_router, abi=ape_router_abi)

contract_sushi_swap = web3.eth.contract(address=sushi_router, abi=sushi_router_abi)

nonce = web3.eth.get_transaction_count(sender_address)

# Code starts here

contract_arbitrage = web3.eth.contract(address = arb_contract_address, abi=arb_contract_abi)

trade_result_1 = 0
trade_result_2 = 0
numberWei = 1 * 10 ** 18

def arb_calculation():
    while True:
        capital = 100

        sushi_wmatic_price = contract_sushi_swap.functions.getAmountsOut(numberWei,[wmatic_address, usdc_address]).call()

        quick_wmatic_price = contract_quick_swap.functions.getAmountsOut(numberWei,[wmatic_address, usdc_address]).call()

        s_wmatic_price = sushi_wmatic_price[1]/10**6
        q_wmatic_price = quick_wmatic_price[1]/10**6

        print(f"quick wmatic price: ${q_wmatic_price}")
        print(f"sushi wmatic price: ${s_wmatic_price}")

        if  s_wmatic_price > q_wmatic_price:
            global trade_result_1

            quick_buy_wmatic = contract_quick_swap.functions.getAmountsOut(1*capital, [usdc_address, wmatic_address]).call()

            capital_sold = quick_buy_wmatic[1] * 10**6

            sushi_sale_usdc = contract_sushi_swap.functions.getAmountsOut(capital_sold,[wmatic_address, usdc_address]).call()

            conversion_sushi_sale = sushi_sale_usdc[1]/10**6

            trade_result_1 = conversion_sushi_sale - capital

            print(f"difference:${s_wmatic_price - q_wmatic_price}")
            print(f"P/L: ${trade_result_1}")
            
        elif q_wmatic_price > s_wmatic_price:
            global trade_result_2

            sushi_buy_wmatic = contract_sushi_swap.functions.getAmountsOut(1*capital, [usdc_address, wmatic_address]).call()

            capital_sold = sushi_buy_wmatic[1] * 10**6

            quick_sale_usdc = contract_quick_swap.functions.getAmountsOut(capital_sold,[wmatic_address, usdc_address]).call()

            conversion_quick_sale = quick_sale_usdc[1]/10**6

            trade_result_2 = conversion_quick_sale - capital

            print(f"difference:${q_wmatic_price - s_wmatic_price}")
            print(f"P/L: ${trade_result_2}")

        if trade_result_1 > 0:
            # Call arbitrage function with direction 1 (buy on quick, sell on sushi) when PROFITABLE
            arbitrage(1)  
            time.sleep(10)
        elif trade_result_2 > 0:
            # Call arbitrage function with direction 2 (buy on sushi, sell on quick) when PROFITABLE
            arbitrage(2)
            time.sleep(10)

        time.sleep(1) 

def arbitrage(_number):
                direction = _number
                arbitrage_swap = contract_arbitrage.functions.Arbitrage(direction).buildTransaction({
                'from': sender_address,
                'nonce': nonce
                })
                signature = web3.eth.account.sign_transaction(arbitrage_swap, private_key = os.environ.get('private_key'))
                tx_token = web3.eth.send_raw_transaction(signature.rawTransaction)
                print("PROFITABLE TRANSACTION PERFORMED.")
                print(web3.toHex(tx_token))

                time.sleep(15)

arb_calculation()
