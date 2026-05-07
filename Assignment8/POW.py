import hashlib
import time

# Simple Resume Data
resume = {
    "name": "Shivraj Darekar",
    "age": 20,
    "college": "VIIT Pune",
    "branch": "CSE (AI)",
    "skills": [
        "Python",
        "Blockchain",
        "MERN Stack",
        "Machine Learning",
        "Solidity"
    ],
    "projects": [
        "AI Resume Analyzer",
        "Blockchain Voting System",
        "Sales Enquiry Dashboard"
    ],
    "cgpa": 8.5,
    "email": "shivraj@example.com"
}

# Block Class
class Block:

    def __init__(self, index, data, previous_hash):

        self.index = index

        self.timestamp = time.time()

        self.data = data

        self.previous_hash = previous_hash

        self.nonce = 0

        self.hash = self.calculate_hash()

    # Generate SHA-256 Hash
    def calculate_hash(self):

        text = (
            str(self.index)
            + str(self.timestamp)
            + str(self.data)
            + str(self.previous_hash)
            + str(self.nonce)
        )

        return hashlib.sha256(text.encode()).hexdigest()

    # Mining Function
    def mine_block(self, difficulty):

        print(f"\nMining Block {self.index}...")

        target = "0" * difficulty

        start_time = time.time()

        attempts = 0

        while self.hash[:difficulty] != target:

            self.nonce += 1

            attempts += 1

            self.hash = self.calculate_hash()

        end_time = time.time()

        print("Block Successfully Mined!")
        print("Nonce Value:", self.nonce)
        print("Hash:", self.hash)
        print("Mining Attempts:", attempts)
        print("Mining Time:", round(end_time - start_time, 4), "seconds")


# Blockchain Class
class Blockchain:

    def __init__(self):

        self.chain = [self.create_genesis_block()]

        self.difficulty = 4

    # Genesis Block
    def create_genesis_block(self):

        return Block(0, "Genesis Block", "0")

    # Latest Block
    def get_latest_block(self):

        return self.chain[-1]

    # Add Block
    def add_block(self, new_block):

        new_block.previous_hash = self.get_latest_block().hash

        new_block.mine_block(self.difficulty)

        self.chain.append(new_block)


# Create Blockchain
my_blockchain = Blockchain()

# Add Resume Block
resume_block = Block(
    1,
    resume,
    my_blockchain.get_latest_block().hash
)

my_blockchain.add_block(resume_block)

# Print Blockchain
print("\n========== BLOCKCHAIN DATA ==========\n")

for block in my_blockchain.chain:

    print("Block Number:", block.index)

    print("Timestamp:", block.timestamp)

    print("Data:", block.data)

    print("Nonce:", block.nonce)

    print("Current Hash:", block.hash)

    print("Previous Hash:", block.previous_hash)

    print("-" * 60)