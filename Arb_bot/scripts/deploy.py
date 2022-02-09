from brownie import network, accounts, config, arbContract2
import os

def main():
    my_account = accounts.add(config['wallets']['from_key'])
    print(my_account)
    arb = arbContract2.deploy(config['networks']['polygon-main']['sushiV2Router'], config['networks']['polygon-main']['quickRouter'], config['networks']['polygon-main']['wmaticAddress'], config['networks']['polygon-main']['usdcAddress'],{'from': my_account})
    print(arb.address)


