# ASSIGNMENT 3A: Data Tampering Detection
# Demonstrates how blockchain detects data tampering through hash comparison

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
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.compute_hash()
    
    # Calculate hash from current data
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
    
    # Check if block has been tampered
    def is_tampered(self):
        stored_hash = self.hash
        current_hash = self.compute_hash()
        is_tampered = (stored_hash != current_hash)
        return is_tampered, stored_hash, current_hash


# Blockchain class
class Blockchain:
    def __init__(self, difficulty=3):
        self.chain = []
        self.difficulty = difficulty
        self.create_genesis_block()
    
    # Create genesis block
    def create_genesis_block(self):
        genesis = Block(0, time.time(), {"message": "Genesis Block"}, "0")
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
        
        while not self.is_valid_proof(block):
            block.nonce += 1
            block.hash = block.compute_hash()
        
        if verbose:
            print("Block mined! Nonce:", block.nonce)
    
    # Add new block
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
    
    # Detect tampering in all blocks
    def detect_tampering(self):
        print("\n" + "="*70)
        print("TAMPERING DETECTION SYSTEM")
        print("="*70)
        print("Scanning blockchain for data tampering...\n")
        
        tampering_found = False
        tampered_blocks = []
        
        for block in self.chain:
            is_tampered, stored, current = block.is_tampered()
            
            print("Block #" + str(block.index) + ":")
            print("  Data:", block.data)
            
            if is_tampered:
                print("  Stored Hash:   ", stored[:40] + "...")
                print("  Calculated Hash:", current[:40] + "...")
                print("  Status: DATA TAMPERED!")
                print("  WARNING: Block has been MODIFIED!")
                tampering_found = True
                tampered_blocks.append(block.index)
            else:
                print("  Hash:", stored[:40] + "...")
                print("  Status: Data Not Tampered")
            print()
        
        print("="*70)
        if tampering_found:
            print("VERDICT: DATA TAMPERED")
            print("Tampered Blocks:", tampered_blocks)
            print("Blockchain integrity COMPROMISED!")
        else:
            print("VERDICT: DATA NOT TAMPERED")
            print("All blocks are valid!")
            print("Blockchain integrity INTACT!")
        print("="*70)
        
        return not tampering_found
    
    # Display blockchain
    def display_chain(self):
        print("\n" + "="*70)
        print("BLOCKCHAIN CONTENTS")
        print("="*70)
        
        for block in self.chain:
            print("\nBlock #" + str(block.index))
            print("  Time:", datetime.fromtimestamp(block.timestamp))
            print("  Data:", block.data)
            print("  Hash:", block.hash)
            print("  Prev:", block.previous_hash[:40] + "...")
            print("  Nonce:", block.nonce)
            print("-" * 70)


# Display menu
def display_menu():
    print("\n" + "="*70)
    print("ASSIGNMENT 3A: DATA TAMPERING DETECTION MENU")
    print("="*70)
    print("1. Add Transaction Block")
    print("2. Display Blockchain")
    print("3. Tamper with Block Data (Simulate Attack)")
    print("4. Detect Tampering")
    print("5. Exit")
    print("="*70)


# Main function
def main():
    print("\n" + "="*70)
    print("ASSIGNMENT 3A: DATA TAMPERING DETECTION")
    print("="*70)
    
    # Initialize blockchain
    blockchain = Blockchain(difficulty=3)
    print("\nBlockchain initialized!")
    print("Genesis block created.")
    
    # Add initial transactions
    print("\nAdding initial transactions...")
    blockchain.add_block({"from": "Alice", "to": "Bob", "amount": 50})
    blockchain.add_block({"from": "Bob", "to": "Carol", "amount": 25})
    blockchain.add_block({"from": "Carol", "to": "David", "amount": 10})
    print("3 transaction blocks added successfully!")
    
    # Main menu loop
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-5): ")
        
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
            print("\nTransaction added successfully!")
            print("Block #" + str(block.index) + " created")
        
        elif choice == "2":
            # Display blockchain
            blockchain.display_chain()
        
        elif choice == "3":
            # Tamper with data
            print("\n" + "-"*70)
            print("SIMULATE DATA TAMPERING")
            print("-"*70)
            
            print("\nAvailable blocks to tamper:")
            for i in range(1, len(blockchain.chain)):
                print("Block #" + str(i) + ":", blockchain.chain[i].data)
            
            try:
                block_num = int(input("\nEnter block number to tamper: "))
                
                if block_num < 1 or block_num >= len(blockchain.chain):
                    print("Invalid block number!")
                    continue
                
                print("\nCurrent data:", blockchain.chain[block_num].data)
                
                print("\nEnter new values:")
                new_sender = input("New sender: ")
                new_receiver = input("New receiver: ")
                new_amount = input("New amount: ")
                
                print("\nTampering with Block #" + str(block_num) + "...")
                blockchain.chain[block_num].data = {
                    "from": new_sender,
                    "to": new_receiver,
                    "amount": new_amount
                }
                
                print("Data tampered successfully!")
                print("New data:", blockchain.chain[block_num].data)
                print("\nNote: Hash was NOT recalculated")
                
            except ValueError:
                print("Invalid input! Please enter a number.")
        
        elif choice == "4":
            # Detect tampering
            blockchain.detect_tampering()
        
        elif choice == "5":
            # Exit
            print("\nExiting program...")
            break
           
        else:
            print("\nInvalid choice! Please enter 1-5.")


# Run program
if __name__ == "__main__":
    main()  




