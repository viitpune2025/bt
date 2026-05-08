# ASSIGNMENT 3B: Hash Pointer Security
# Demonstrates hash pointers, tampering with re-mining, and chain link validation

import hashlib
import json
import time
from datetime import datetime

# Generate SHA-256 hash
def sha256(data):
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


# Block class
class Block:
    def __init__(self, index, timestamp, data, previous_hash, nonce=0):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash  # Hash pointer to previous block
        self.nonce = nonce
        self.hash = self.compute_hash()
    
    # Calculate hash
    def compute_hash(self):
        block_data = {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }
        block_string = json.dumps(block_data, sort_keys=True, separators=(",", ":"))
        return sha256(block_string)


# Blockchain class
class Blockchain:
    def __init__(self, difficulty=3):
        self.chain = []
        self.difficulty = difficulty
        self.create_genesis_block()
    
    # Create genesis block
    def create_genesis_block(self):
        genesis = Block(0, time.time(), {"message": "Genesis"}, "0")
        self.mine_block(genesis, verbose=False)
        self.chain.append(genesis)
    
    @property
    def last_block(self):
        return self.chain[-1]
    
    # Check if hash meets difficulty
    def is_valid_proof(self, block):
        return block.hash.startswith("0" * self.difficulty)
    
    # Mine block
    def mine_block(self, block, verbose=True):
        if verbose:
            print("Mining block... Please wait...")
        
        block.nonce = 0
        while not self.is_valid_proof(block):
            block.nonce += 1
            block.hash = block.compute_hash()
        
        if verbose:
            print("Block mined! Nonce:", block.nonce)
    
    # Add block
    def add_block(self, data):
        new_block = Block(
            self.last_block.index + 1,
            time.time(),
            data,
            self.last_block.hash
        )
        self.mine_block(new_block)
        self.chain.append(new_block)
        return new_block
    
    # Validate hash pointers (check if blocks are properly linked)
    def validate_hash_pointers(self):
        print("\n" + "="*70)
        print("HASH POINTER VALIDATION")
        print("="*70)
        print("Checking chain links (hash pointers)...\n")
        
        all_valid = True
        broken_links = []
        
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            
            print("Link: Block " + str(i-1) + " -> Block " + str(i))
            print("  Block " + str(i-1) + " hash:    ", previous.hash[:40] + "...")
            print("  Block " + str(i) + " prev_hash:", current.previous_hash[:40] + "...")
            
            if current.previous_hash == previous.hash:
                print("  Status: Link Valid\n")
            else:
                print("  Status: LINK BROKEN!")
                print("  Hash pointer mismatch detected!\n")
                all_valid = False
                broken_links.append(str(i-1) + "->" + str(i))
        
        print("="*70)
        if all_valid:
            print("RESULT: All hash pointers VALID")
            print("Chain integrity intact!")
        else:
            print("RESULT: BROKEN HASH POINTERS DETECTED")
            print("Broken links:", broken_links)
            print("Chain integrity COMPROMISED!")
        print("="*70)
        
        return all_valid
    
    # Display blockchain
    def display_chain(self):
        print("\n" + "="*70)
        print("BLOCKCHAIN CONTENTS")
        print("="*70)
        
        for i, block in enumerate(self.chain):
            link_status = ""
            if i > 0:
                if block.previous_hash == self.chain[i-1].hash:
                    link_status = "Linked"
                else:
                    link_status = "BROKEN"
            
            print("\nBlock #" + str(block.index))
            print("  Data:", block.data)
            print("  Hash:", block.hash[:40] + "...")
            print("  Prev:", block.previous_hash[:40] + "...")
            if link_status:
                print("  Link:", link_status)
            print("-" * 70)


# Display menu
def display_menu():
    print("\n" + "="*70)
    print("ASSIGNMENT 3B: HASH POINTER SECURITY MENU")
    print("="*70)
    print("1. Add Transaction Block")
    print("2. Display Blockchain")
    print("3. Tamper WITHOUT Re-mining")
    print("4. Tamper WITH Re-mining (Smart Attack)")
    print("5. Validate Hash Pointers")
    print("6. Exit")
    print("="*70)


# Main function
def main():
    print("\n" + "="*70)
    print("ASSIGNMENT 3B: HASH POINTER SECURITY")
    print("="*70)
    
    # Initialize blockchain
    blockchain = Blockchain(difficulty=3)
    print("\nBlockchain initialized!")
    
    # Add initial transactions
    print("\nAdding initial transactions...")
    blockchain.add_block({"from": "Alice", "to": "Bob", "amount": 50})
    blockchain.add_block({"from": "Bob", "to": "Carol", "amount": 25})
    blockchain.add_block({"from": "Carol", "to": "David", "amount": 10})
    print("3 blocks added successfully!")
    
    # Main menu loop
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-6): ")
        
        if choice == "1":
            # Add transaction
            print("\n" + "-"*70)
            print("ADD TRANSACTION")
            print("-"*70)
            
            sender = input("Enter sender: ")
            receiver = input("Enter receiver: ")
            amount = input("Enter amount: ")
            
            transaction = {"from": sender, "to": receiver, "amount": amount}
            
            block = blockchain.add_block(transaction)
            print("\nTransaction added!")
            print("Block #" + str(block.index) + " created")
        
        elif choice == "2":
            # Display blockchain
            blockchain.display_chain()
        
        elif choice == "3":
            # Tamper without re-mining
            print("\n" + "-"*70)
            print("TAMPER WITHOUT RE-MINING")
            print("-"*70)
            
            print("\nAvailable blocks:")
            for i in range(1, len(blockchain.chain)):
                print("Block #" + str(i) + ":", blockchain.chain[i].data)
            
            try:
                block_num = int(input("\nEnter block number: "))
                
                if block_num < 1 or block_num >= len(blockchain.chain):
                    print("Invalid block number!")
                    continue
                
                print("\nCurrent data:", blockchain.chain[block_num].data)
                
                new_amount = input("Enter new amount: ")
                
                original_hash = blockchain.chain[block_num].hash
                
                blockchain.chain[block_num].data["amount"] = new_amount
                
                print("\nData tampered!")
                print("New data:", blockchain.chain[block_num].data)
                print("Hash NOT recalculated")
                print("\nOriginal hash:", original_hash[:40] + "...")
                print("Current hash: ", blockchain.chain[block_num].hash[:40] + "...")
                
            except ValueError:
                print("Invalid input!")
        
        elif choice == "4":
            # Tamper with re-mining
            print("\n" + "-"*70)
            print("SMART ATTACK: TAMPER WITH RE-MINING")
            print("-"*70)
            
            print("\nAvailable blocks:")
            for i in range(1, len(blockchain.chain)):
                print("Block #" + str(i) + ":", blockchain.chain[i].data)
            
            try:
                block_num = int(input("\nEnter block number: "))
                
                if block_num < 1 or block_num >= len(blockchain.chain):
                    print("Invalid block number!")
                    continue
                
                print("\nCurrent data:", blockchain.chain[block_num].data)
                
                new_amount = input("Enter new amount: ")
                
                original_hash = blockchain.chain[block_num].hash
                
                print("\nStep 1: Tampering with data...")
                blockchain.chain[block_num].data["amount"] = new_amount
                print("Data changed!")
                
                print("\nStep 2: Re-mining block...")
                blockchain.mine_block(blockchain.chain[block_num])
                
                print("\nAttack complete!")
                print("Original hash:", original_hash[:40] + "...")
                print("New hash:     ", blockchain.chain[block_num].hash[:40] + "...")
                print("\nBlock has valid hash but chain link is broken!")
                
            except ValueError:
                print("Invalid input!")
        
        elif choice == "5":
            # Validate hash pointers
            blockchain.validate_hash_pointers()
        
        elif choice == "6":
            # Exit
            print("\nExiting program...")   
            break
        
        else:
            print("\nInvalid choice! Please enter 1-6.")


# Run program
if __name__ == "__main__":
    main()