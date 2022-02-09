from brownie import accounts, interface, config, arbContract2

def main():
    my_account = accounts.add(config['wallets']['from_key'])

    arb_contract = arbContract2[len(arbContract2) - 1]

    tx = arb_contract.Arbitrage(1, {"from": my_account})

    # tx = arb_contract.withdrawAll("0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",  {"from": my_account})

    print(tx.txid)




