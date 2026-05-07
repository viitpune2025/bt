# README - Assignment 5

# Assignment 5

## Deploy a Simple HelloWorld Smart Contract on Ethereum Test Network

---

# Aim

To create and deploy a simple Solidity smart contract named `HelloWorld` on the Ethereum blockchain using Remix IDE and MetaMask.

---

# Objective

* Learn basics of Ethereum smart contracts
* Understand Solidity programming
* Deploy smart contracts on blockchain
* Interact with deployed contract

---

# Software Requirements

* Remix IDE
* MetaMask Wallet
* Internet Connection
* Ethereum Sepolia Testnet OR Ganache

---

# Theory

A Smart Contract is a self-executing program stored on the blockchain. Once deployed, it runs automatically and securely without needing a central authority.

Ethereum uses Solidity programming language for creating smart contracts.

In this assignment, a simple HelloWorld smart contract is deployed which stores a message on blockchain.

---

# Smart Contract Code

```solidity
// SPDX-License-Identifier: MIT
pragma solidity >=0.7.0 <0.9.0;

contract HelloWorld {

    string public message;

    constructor() {
        message = "Hello Blockchain";
    }

    function setMessage(string memory newMessage) public {
        message = newMessage;
    }
}
```

---

# Code Explanation

## SPDX License

```solidity
// SPDX-License-Identifier: MIT
```

Defines software license.

---

## Solidity Version

```solidity
pragma solidity >=0.7.0 <0.9.0;
```

Specifies compiler version.

---

## Contract Declaration

```solidity
contract HelloWorld
```

Creates a smart contract named `HelloWorld`.

---

## State Variable

```solidity
string public message;
```

Stores message on blockchain.

---

## Constructor

```solidity
constructor() {
    message = "Hello Blockchain";
}
```

Runs once during deployment and initializes the message.

---

## setMessage Function

```solidity
function setMessage(string memory newMessage) public
```

Updates message stored in smart contract.

---

# Procedure

1. Open Remix IDE
2. Create `HelloWorld.sol`
3. Paste Solidity code
4. Compile contract using Solidity compiler
5. Connect MetaMask wallet
6. Select Injected Provider
7. Deploy contract
8. Interact with deployed functions

---

# Expected Output

* Contract deployed successfully
* Initial message displayed:

```text
Hello Blockchain
```

* Message updates successfully using `setMessage()`

---

# Result

The HelloWorld smart contract was successfully deployed and executed on Ethereum blockchain.

---

# Conclusion

This assignment demonstrates the basic process of creating, compiling, deploying, and interacting with a Solidity smart contract on Ethereum blockchain.
