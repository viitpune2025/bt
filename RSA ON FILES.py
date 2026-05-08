# ASSIGNMENT 4B: RSA File Encryption (8-bit format, M=256)
# This program demonstrates RSA encryption for files byte-by-byte

import random
import os

# Function to calculate GCD
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

# Function to calculate modular inverse
def mod_inverse(e, phi):
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd_val, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd_val, x, y
    
    _, x, _ = extended_gcd(e, phi)
    return (x % phi + phi) % phi

# Function to check if number is prime
def is_prime(n, k=5):
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False
    
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        
        if x == 1 or x == n - 1:
            continue
        
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    
    return True

# Function to generate prime number
def generate_prime(bits=8):
    while True:
        num = random.getrandbits(bits)
        if num < 2:
            continue
        if num % 2 == 0:
            num += 1
        if is_prime(num):
            return num


# RSA class for file encryption
class RSA_File:
    def __init__(self):
        # Use 8-bit primes for M=256 format
        self.key_size = 8
        self.public_key = None
        self.private_key = None
        self.n = None
        self.generate_keys()
    
    # Generate RSA keys for file encryption
    def generate_keys(self):
        print("\nGenerating RSA keys for file encryption (8-bit format)...")
        
        # Generate primes
        p = generate_prime(self.key_size)
        q = generate_prime(self.key_size)
        
        while p == q:
            q = generate_prime(self.key_size)
        
        print("Prime p:", p)
        print("Prime q:", q)
        
        # Calculate n
        self.n = p * q   
        print("n = p * q =", self.n)
        
        # Must ensure n > 255 for M=256
        if self.n <= 255:   
            print("Warning: n is too small, regenerating keys...")
            return self.generate_keys()
        
        print("n is", self.n, "(greater than 255, suitable for byte encryption)")

        # Calculate phi
        phi = (p - 1) * (q - 1)
        print("phi(n) =", phi)
        
        # Choose e
        e = 65537
        if e >= phi:
            e = 3
            while gcd(e, phi) != 1:
                e += 2
        
        print("Public exponent e:", e)
        
        # Calculate d
        d = mod_inverse(e, phi)
        print("Private exponent d:", d)
        
        # Store keys
        self.public_key = (e, self.n)
        self.private_key = (d, self.n)
        
        print("\nKeys generated successfully!")
        print("Public Key: (" + str(e) + ", " + str(self.n) + ")")
        print("Private Key: (" + str(d) + ", " + str(self.n) + ")")
    
    # Encrypt a single byte
    def encrypt_byte(self, byte_value):
        if byte_value >= self.n:
            # If byte is larger than n, use modulo
            byte_value = byte_value % self.n
        
        e, n = self.public_key
        encrypted = pow(byte_value, e, n)
        return encrypted
    
    # Decrypt a single value
    def decrypt_byte(self, encrypted_value):
        d, n = self.private_key
        decrypted = pow(encrypted_value, d, n)
        return decrypted
    
    # Encrypt entire file
    def encrypt_file(self, input_filename, output_filename):
        print("\n" + "="*70)
        print("FILE ENCRYPTION")
        print("="*70)
        
        # Check if file exists
        if not os.path.exists(input_filename):
            print("Error: File not found!")
            return False
        
        print("Input file:", input_filename)
        print("Output file:", output_filename)
        
        # Read file as bytes
        print("\nReading file as bytes...")
        with open(input_filename, 'rb') as f:
            file_data = f.read()
        
        print("File size:", len(file_data), "bytes")
        print("First 10 bytes:", list(file_data[:10]))
        
        # Encrypt each byte
        print("\nEncrypting bytes...")
        encrypted_data = []
        
        for i, byte in enumerate(file_data):
            encrypted_byte = self.encrypt_byte(byte)
            encrypted_data.append(encrypted_byte)
            
            # Show progress every 10 bytes
            if (i + 1) % 10 == 0:
                print("  Encrypted", i + 1, "bytes...", end='\r')
        
        print("\nAll", len(file_data), "bytes encrypted successfully!")
        
        # Save encrypted data
        # Format: comma-separated values
        print("\nSaving encrypted data to file...")
        with open(output_filename, 'w') as f:
            encrypted_string = ','.join(map(str, encrypted_data))
            f.write(encrypted_string)
        
        print("Encrypted file saved successfully!")
        print("\nEncryption complete!")
        print("="*70)
        return True
    
    # Decrypt entire file
    def decrypt_file(self, input_filename, output_filename):
        print("\n" + "="*70)
        print("FILE DECRYPTION")
        print("="*70)
        
        # Check if file exists
        if not os.path.exists(input_filename):
            print("Error: File not found!")
            return False
        
        print("Input file (encrypted):", input_filename)
        print("Output file (decrypted):", output_filename)
        
        # Read encrypted data
        print("\nReading encrypted data...")
        with open(input_filename, 'r') as f:
            encrypted_string = f.read()
        
        # Parse comma-separated values
        encrypted_data = list(map(int, encrypted_string.split(',')))
        print("Number of encrypted values:", len(encrypted_data))
        
        # Decrypt each value
        print("\nDecrypting bytes...")
        decrypted_bytes = []
        
        for i, encrypted_value in enumerate(encrypted_data):
            decrypted_byte = self.decrypt_byte(encrypted_value)
            decrypted_bytes.append(decrypted_byte)
            
            # Show progress
            if (i + 1) % 10 == 0:
                print("  Decrypted", i + 1, "bytes...", end='\r')
        
        print("\nAll", len(encrypted_data), "bytes decrypted successfully!")
        
        # Save decrypted data as bytes
        print("\nSaving decrypted data to file...")
        with open(output_filename, 'wb') as f:
            f.write(bytes(decrypted_bytes))
        
        print("Decrypted file saved successfully!")
        print("\nDecryption complete!")
        print("="*70)
        return True
    
    # Verify file integrity
    def verify_files(self, original_file, decrypted_file):
        print("\n" + "="*70)
        print("FILE INTEGRITY VERIFICATION")
        print("="*70)
        
        # Read both files
        with open(original_file, 'rb') as f:
            original_data = f.read()
        
        with open(decrypted_file, 'rb') as f:
            decrypted_data = f.read()
        
        print("Original file size:", len(original_data), "bytes")
        print("Decrypted file size:", len(decrypted_data), "bytes")
        
        # Compare
        if original_data == decrypted_data:
            print("\nStatus: SUCCESS")
            print("Files are IDENTICAL!")
            print("Encryption and decryption worked perfectly!")
        else:
            print("\nStatus: FAILED")
            print("Files are DIFFERENT!")
            print("Something went wrong in encryption/decryption")
        
        print("="*70)


# Display menu
def display_menu():
    print("\n" + "="*70)
    print("ASSIGNMENT 4B: RSA FILE ENCRYPTION - MENU")
    print("="*70)
    print("1. Create Sample Text File")
    print("2. Display RSA Keys")
    print("3. Encrypt File")
    print("4. Decrypt File")
    print("5. Verify File Integrity")
    print("6. Exit")
    print("="*70)


# Main function
def main():
    print("\n" + "="*70)
    print("ASSIGNMENT 4B: RSA FILE ENCRYPTION (8-bit format, M=256)")
    print("="*70)
    print("\nThis program encrypts files byte-by-byte using RSA")
    print("Each byte (0-255) is encrypted individually")
    
    # Initialize RSA for file encryption
    rsa = RSA_File()
    
    # Variables to track files
    original_file = None
    encrypted_file = None
    decrypted_file = None
    
    # Main menu loop
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-6): ")
        
        if choice == "1":
            # Create sample file
            print("\n" + "-"*70)
            print("CREATE SAMPLE TEXT FILE")
            print("-"*70)
            
            filename = input("Enter filename (e.g., message.txt): ")
            
            print("\nEnter file content (press Enter twice when done):")
            lines = []
            while True:
                line = input()
                if line == "":
                    break
                lines.append(line)
            
            content = '\n'.join(lines)
            
            if content:
                # Save file
                with open(filename, 'w') as f:
                    f.write(content)
                
                print("\nFile created successfully!")
                print("Filename:", filename)
                print("Size:", len(content), "characters")
                print("\nContent:")
                print(content)
                
                original_file = filename
            else:
                print("No content entered. File not created.")
        
        elif choice == "2":
            # Display keys
            print("\n" + "="*70)
            print("RSA KEYS FOR FILE ENCRYPTION")
            print("="*70)
            
            e, n = rsa.public_key
            d, n2 = rsa.private_key
            
            print("\nPublic Key:")
            print("  e =", e)
            print("  n =", n)
            
            print("\nPrivate Key:")
            print("  d =", d)
            print("  n =", n2)
            
            print("\nNote: n =", n, "(must be > 255 for byte encryption)")
            print("="*70)
        
        elif choice == "3":
            # Encrypt file
            print("\n" + "-"*70)
            print("ENCRYPT FILE")
            print("-"*70)
            
            input_file = input("Enter input filename: ")
            output_file = input("Enter output filename for encrypted data: ")
            
            if rsa.encrypt_file(input_file, output_file):
                encrypted_file = output_file
                if original_file is None:
                    original_file = input_file
        
        elif choice == "4":
            # Decrypt file
            print("\n" + "-"*70)
            print("DECRYPT FILE")
            print("-"*70)
            
            input_file = input("Enter encrypted filename: ")
            output_file = input("Enter output filename for decrypted data: ")
            
            if rsa.decrypt_file(input_file, output_file):
                decrypted_file = output_file
        
        elif choice == "5":
            # Verify integrity
            print("\n" + "-"*70)
            print("VERIFY FILE INTEGRITY")
            print("-"*70)
            
            if original_file and decrypted_file:
                rsa.verify_files(original_file, decrypted_file)
            else:
                print("\nYou need to:")
                print("1. Create or select original file")
                print("2. Encrypt it")
                print("3. Decrypt it")
                print("4. Then verify")
        
        elif choice == "6":
            # Exit
            print("\nThank you for using RSA file encryption!")
            print("Exiting...")
            break
        
        else:
            print("\nInvalid choice! Please enter 1-6")


# Run the program
if __name__ == "__main__":
    main()