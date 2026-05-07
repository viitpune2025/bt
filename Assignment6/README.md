# README - Assignment 6

# Assignment 6

## Write and Execute a Solidity Smart Contract to Transfer Tokens Between Accounts

---

# Aim

To create and execute a Solidity smart contract that transfers tokens securely between Ethereum accounts.

---

# Objective

* Learn token creation using Solidity
* Understand blockchain transactions
* Implement token transfer functionality
* Manage balances using smart contracts

---

# Software Requirements

* Remix IDE
* MetaMask Wallet OR Ganache
* Solidity Compiler

---

# Theory

A token smart contract is used to create digital assets on blockchain. Tokens can be transferred between users securely using Ethereum smart contracts.

In this assignment, a custom token named `CollegeToken` is created. The smart contract stores balances and allows token transfer between accounts.

---

# Smart Contract Code

```solidity
// SPDX-License-Identifier: MIT
pragma solidity >=0.7.0 <0.9.0;

contract SimpleToken {

    string public name = "CollegeToken";
    string public symbol = "CLG";

    uint8 public decimals = 0;

    uint256 public totalSupply;

    mapping(address => uint256) public balanceOf;

    event Transfer(
        address indexed from,
        address indexed to,
        uint256 value
    );

    constructor(uint256 _initialSupply) {

        totalSupply = _initialSupply;

        balanceOf[msg.sender] = _initialSupply;
    }

    function transfer(address _to, uint256 _value)
        public
        returns (bool)
    {

        require(_to != address(0), "Invalid receiver");

        require(
            balanceOf[msg.sender] >= _value,
            "Insufficient balance"
        );

        balanceOf[msg.sender] -= _value;

        balanceOf[_to] += _value;

        emit Transfer(msg.sender, _to, _value);

        return true;
    }
}
```

---

# Code Explanation

## Token Name

```solidity
string public name = "CollegeToken";
```

Defines token name.

---

## Token Symbol

```solidity
string public symbol = "CLG";
```

Defines token symbol.

---

## Decimals

```solidity
uint8 public decimals = 0;
```

Specifies token decimal places.

---

## Total Supply

```solidity
uint256 public totalSupply;
```

Stores total tokens available.

---

## Mapping

```solidity
mapping(address => uint256) public balanceOf;
```

Stores balance of every Ethereum account.

---

## Event

```solidity
event Transfer(...)
```

Logs token transfer transactions.

---

## Constructor

```solidity
constructor(uint256 _initialSupply)
```

Runs during deployment and gives all tokens to deployer.

---

## Transfer Function

```solidity
function transfer(address _to, uint256 _value)
```

Transfers tokens from sender to receiver.

---

## require()

```solidity
require(balanceOf[msg.sender] >= _value)
```

Checks whether sender has enough balance.

---

# Procedure

1. Open Remix IDE
2. Create `SimpleToken.sol`
3. Paste Solidity code
4. Compile smart contract
5. Deploy contract with initial supply value
6. Check initial balance using `balanceOf()`
7. Transfer tokens using `transfer()`
8. Verify updated balances

---

# Example Execution

## Initial Supply

```text
1000
```

## Initial Balance

```text
Owner = 1000
```

## Transfer

```text
Transfer 100 tokens
```

## Final Balances

```text
Sender = 900
Receiver = 100
```

---

# Expected Output

* Smart contract deployed successfully
* Tokens transferred successfully
* Balances updated correctly

---

# Result

The token transfer smart contract was successfully created and executed on Ethereum blockchain.

---

# Conclusion

This assignment demonstrates token creation, token transfer, balance management, and transaction validation using Solidity smart contracts on blockchain.
