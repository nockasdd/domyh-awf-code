---
name: solidity
detect: ["*.sol", "hardhat.config.js", "hardhat.config.ts", "foundry.toml"]
version: "6.2.3"
category: blockchain
tier: 2
---

# Solidity Patterns — DOMYH Awesome Code

> **Version**: Solidity 0.8.24+ (2025-2026)
> **Frameworks**: Hardhat, Foundry
> **Philosophy**: Security-first, gas-efficient

---

## 🎯 When to Use

Use for: Smart contracts, DeFi, NFTs, DAOs on EVM chains.
**NOT for**: Off-chain logic, non-blockchain apps.

---

## 🔧 Project Setup

### Foundry (Recommended)

```bash
forge init my-project
cd my-project
forge build
forge test
```

### Hardhat

```bash
npx hardhat init
npm install @openzeppelin/contracts
npx hardhat compile
```

---

## 🔄 Core Patterns

### ERC20 Token

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract MyToken is ERC20, Ownable {
    constructor() ERC20("MyToken", "MTK") Ownable(msg.sender) {}

    function mint(address to, uint256 amount) public onlyOwner {
        _mint(to, amount);
    }
}
```

### Security Patterns

```solidity
// ✅ Checks-Effects-Interactions
function withdraw(uint256 amount) external {
    // Checks
    require(balances[msg.sender] >= amount, "Insufficient");

    // Effects
    balances[msg.sender] -= amount;

    // Interactions
    (bool success, ) = msg.sender.call{value: amount}("");
    require(success, "Transfer failed");
}

// ✅ Reentrancy Guard
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

contract Secure is ReentrancyGuard {
    function safeWithdraw() external nonReentrant {
        // ...
    }
}

// ✅ Access Control
import "@openzeppelin/contracts/access/AccessControl.sol";

contract MyContract is AccessControl {
    bytes32 public constant ADMIN = keccak256("ADMIN");

    function adminOnly() external onlyRole(ADMIN) {
        // ...
    }
}
```

### Gas Optimization

```solidity
// ✅ Pack storage variables
contract Optimized {
    // Packed into 1 slot (32 bytes)
    uint128 public value1;  // 16 bytes
    uint64 public value2;   // 8 bytes
    uint32 public value3;   // 4 bytes
    bool public flag;       // 1 byte
}

// ✅ Use calldata for external
function process(bytes calldata data) external pure returns (bytes32) {
    return keccak256(data);
}

// ✅ Unchecked for safe math
function sum(uint256[] calldata nums) external pure returns (uint256 total) {
    uint256 len = nums.length;
    for (uint256 i; i < len; ) {
        unchecked {
            total += nums[i];
            ++i;
        }
    }
}
```

---

## 🧪 Testing with Foundry

```solidity
// test/MyToken.t.sol
import "forge-std/Test.sol";
import "../src/MyToken.sol";

contract MyTokenTest is Test {
    MyToken token;
    address alice = makeAddr("alice");

    function setUp() public {
        token = new MyToken();
    }

    function test_Mint() public {
        token.mint(alice, 1000e18);
        assertEq(token.balanceOf(alice), 1000e18);
    }

    function testFuzz_Transfer(uint256 amount) public {
        vm.assume(amount > 0 && amount <= 1000e18);
        token.mint(address(this), amount);
        token.transfer(alice, amount);
        assertEq(token.balanceOf(alice), amount);
    }
}
```

---

## ✅ Production Checklist

### Security

- [ ] Slither static analysis
- [ ] Aderyn audit
- [ ] Reentrancy protection
- [ ] Integer overflow handled

### Quality

- [ ] 100% test coverage
- [ ] Fuzz testing
- [ ] Gas optimization
- [ ] Events for state changes

### Deploy

- [ ] Multisig ownership
- [ ] Verified on Etherscan
- [ ] Upgrade path planned

---

_DOMYH Awesome Code • Solidity 0.8.24+_
