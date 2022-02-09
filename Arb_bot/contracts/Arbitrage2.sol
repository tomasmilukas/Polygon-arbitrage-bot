// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.6.6;

import "./IUniswapV2Router02.sol";
import { IERC20 } from "./Interfaces.sol";
import "./IWETH.sol";
import "./Withdrawable.sol";

contract arbContract2 is Ownable{

    struct TradeDirection{  
        uint directionNumber;
    }

    IUniswapV2Router02 quick_router;
    IUniswapV2Router02 sushi_router;
    IERC20 usdc;
    IWETH wmatic;
    TradeDirection public tradeDirection;

    event Received(address sender, uint amount);

    receive() external payable {
    emit Received(msg.sender, msg.value);
    }

    constructor(
        address sushiAddress,
        address quickAddress,
        address wmaticAddress,
        address usdcAddress
        ) public {
        sushi_router = IUniswapV2Router02(sushiAddress);
        quick_router = IUniswapV2Router02(quickAddress);
        wmatic = IWETH(wmaticAddress);
        usdc = IERC20(usdcAddress);
    }

    function deposit() external payable {}   

    function Arbitrage(uint _direction) public payable onlyOwner{
    
    tradeDirection.directionNumber = _direction;
    uint256 usdcBalance = usdc.balanceOf(address(this));

    if (tradeDirection.directionNumber == 1){

            // USDC -> WMATIC on quickswap
            usdc.approve(address(quick_router), usdcBalance);
            address[] memory direction_quick = new address[] (2);
            direction_quick[0] = address(usdc);
            direction_quick[1] = address(wmatic);
            uint[] memory minOut_quick = quick_router.getAmountsOut(usdcBalance, direction_quick);
            uint minOut_quick1 = minOut_quick[0] * 97;
            uint minOut_quick2 = minOut_quick1 / 100;
            quick_router.swapExactTokensForETH(usdcBalance, minOut_quick2, direction_quick, address(this), now);

            // WMATIC -> USDC on sushi

            address[] memory direction_sushi = new address[] (2);
            direction_sushi[0] = address(wmatic);
            direction_sushi[1] = address(usdc);
            uint[] memory minOut_sushi = sushi_router.getAmountsOut(usdcBalance, direction_sushi);
            uint minOut_sushi1 = minOut_sushi[0] * 97;
            uint minOut_sushi2 = minOut_sushi1 / 100;
            sushi_router.swapExactETHForTokens{value: address(this).balance}(minOut_sushi2, direction_sushi, address(this), now);
            
    } else {

        // USDC -> WMATIC on sushiswap
            usdc.approve(address(sushi_router), usdcBalance);
            address[] memory direction_sushi = new address[] (2);
            direction_sushi[0] = address(usdc);
            direction_sushi[1] = address(wmatic);
            uint[] memory minOut_sushi = sushi_router.getAmountsOut(usdcBalance, direction_sushi);
            uint minOut_sushi1 = minOut_sushi[0] * 97;
            uint minOut_sushi2 = minOut_sushi1 / 100;
            sushi_router.swapExactTokensForETH(usdcBalance, minOut_sushi2, direction_sushi, address(this), now);

            // WMATIC -> USDC on quickswap

            address[] memory direction_quick = new address[] (2);
            direction_quick[0] = address(wmatic);
            direction_quick[1] = address(usdc);
            uint[] memory minOut_quick = quick_router.getAmountsOut(usdcBalance, direction_quick);
            uint minOut_quick1 = minOut_quick[0] * 97;
            uint minOut_quick2 = minOut_quick1 / 100;
            quick_router.swapExactETHForTokens{value: address(this).balance}(minOut_quick2, direction_quick, address(this), now);
    }
    }

    function withdrawToken(address _tokenContract, uint256 _amount) external onlyOwner {
    IERC20 tokenContract = IERC20(_tokenContract);
    tokenContract.transfer(msg.sender, _amount);
    }

    function withdrawAll(address _tokenAddress) external onlyOwner{
        IERC20 tokenContract = IERC20(_tokenAddress);
        uint256 totalBalance = tokenContract.balanceOf(address(this));
        tokenContract.transfer(msg.sender, totalBalance);
    }

    
}