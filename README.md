# Polygon WMATIC-USDC arbitrage bot

After writing an in-depth article on DeFi lending (https://tomasmilukasblog.com/defi-lending-in-depth-fc5c77f9101d) and uncovering flash loans, I couldn't wait to create and test arbitrage bots. Hence, this is why I started the project.

This is a simple arbitrage bot that trades WMATIC and USDC when there is a a profitable opportunity on the Polygon chain. The reason for deploying the bot on the polygon chain is because the gas fees are far lower than on the majority of other Layer 1 chains and also because it has fewer competitors going after the same opportunities. The two AMMs used to find arbitrage opportunities are Quickswap and Sushiswap.

If you are curious about the bot's results, here are the relevant details:
The arbitrage contracts address: 0x7b6B9662358cBA054DDeD9409FA6Bc343F03c229
The polygonscan link to the contract: https://polygonscan.com/address/0x7b6b9662358cba054dded9409fa6bc343f03c229

Ultimately, the bot was not profitable and I will cover how I will tackle that in the future in the Next Steps section.

Preview of a transaction:

![Polygon USDC -> WMATIC arbitrage bot between QuickSwap and SushiSwap](https://ibb.co/m9Lf4Tx "Polygon USDC -> WMATIC arbitrage bot between QuickSwap and SushiSwap")

## Table of contents

* [Technologies](#technologies)
* [Setup](#setup)
* [Next steps](#next-steps)

## Technologies

The contracts were coded with **Solidity**.
The bot execution and API calls were done with **Python**.
The API calls were done on Infura.
The server for the bot was rented on Heroku.
	
## Setup

The main two folders within this structure are the contracts and scripts folder. The contracts folder holds the main Solidity contracts necessary for the swaps and the scripts folder contains the Python files to deploy and call the contract.

The main contract file is **Arbitrage2.sol** which executes a swap from quick to sushi if the tradedirection is set to 1, and if it is set to any other number, it executes a trade from sushi to quick. The rest of the contracts are added for the swaps, or additional modifiers.

The **deploy.py** is the file that will deploy the contract. However, the main execution file is **realbot.py** which will perform the **arb_calculation()** function every second by calling the relevant contracts and if there is a profitable opportunity after the calculations, the transaction will be executed by calling the **arbitrage(_number)** function.

If you wish to run this bot, you will need to fork the repo, then add a ".env" file with your private key and an Infura API that can call the Polygon Mainnet chain.
Once that is set up, you must deploy the contract with deploy.py, and lastly run the realbot.py in your console. You can see the potential profit (or loss) printed each second in the console. However, this bot is NOT profitable, so I suggest to only fund it with a minuscule amount.


## Next steps

It is still hard for me to pinpoint why this bot is unprofitable. The calculations to achieve profit were pretty strict as I was using **getAmountsOut()** instead of doing my own calculations with getReserves(). The getAmountsOut() function gives the specific price that one would get by trading directly on the AMMs. However, after digging deeper, it seems that the main culprit is probably the speed of the execution bot. 

Hence, the opportunity was already gone after I reached it or I was frontrun when I performed the tx. There are a couple of ways to solve this. However, when I was investigating the block that my transaction occured in, I couldn't find a frontrunning transaction, as there would've been a total loss including thegas cost, and I was excluding the gas cost in my calculations just to achieve basic profitability and improving my bot from there.

Hence, to improve the speed of the transaction, I will need to use BOR (GETH equivalent but for Polygon) to achieve a successful transaction. If that doesn't work, then I will be investigating if there is an error in my calculations or in my logic that prevents me from achieving a profitable arbitrage bot.






