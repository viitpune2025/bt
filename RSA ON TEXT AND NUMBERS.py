# ASSIGNMENT 4A: RSA Encryption on Text and Numbers
# This program demonstrates RSA encryption and decryption for numbers and text

import random

# Function to calculate greatest common divisor
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

# Function to calculate modular inverse
# Find d such that (d * e) mod phi = 1
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
    
    # Miller-Rabin primality test
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

# Function to generate random prime number
def generate_prime(bits=16):
    while True:
        num = random.getrandbits(bits)
        if num < 2:
            continue
        if num % 2 == 0:
            num += 1
        if is_prime(num):
            return num


# RSA class for text and number encryption
class RSA:
    def __init__(self, key_size=16):
        self.key_size = key_size
        self.public_key = None
        self.private_key = None
        self.n = None
        self.generate_keys()
    
    # Generate RSA key pair
    def generate_keys(self):
        print("\nGenerating RSA keys...")
        
        # Step 1: Generate two prime numbers
        p = generate_prime(self.key_size)
        q = generate_prime(self.key_size)
        
        # Make sure p and q are different
        while p == q:
            q = generate_prime(self.key_size)
        
        print("Step 1: Generated prime numbers")
        print("  p =", p)
        print("  q =", q)
        
        # Step 2: Calculate n
        self.n = p * q
        print("\nStep 2: Calculate n = p * q")
        print("  n =", self.n)
        
        # Step 3: Calculate phi
        phi = (p - 1) * (q - 1)
        print("\nStep 3: Calculate phi(n) = (p-1) * (q-1)")
        print("  phi(n) =", phi)
        
        # Step 4: Choose public exponent e
        e = 65537
        if e >= phi:
            e = 3
            while gcd(e, phi) != 1:   
                e += 2
        
        print("\nStep 4: Choose public exponent e")
        print("  e =", e)
        
        # Step 5: Calculate private exponent d
        d = mod_inverse(e, phi)
        print("\nStep 5: Calculate private exponent d")
        print("  d =", d)
        
        # Store keys
        self.public_key = (e, self.n)
        self.private_key = (d, self.n)
        
        print("\nKeys generated successfully!")
        print("Public Key: (e=" + str(e) + ", n=" + str(self.n) + ")")
        print("Private Key: (d=" + str(d) + ", n=" + str(self.n) + ")")
    
    # Encrypt a number
    def encrypt_number(self, message):
        if message >= self.n:
            raise ValueError("Message must be less than n")
        
        e, n = self.public_key
        # Encryption formula: C = M^e mod n
        ciphertext = pow(message, e, n)
        return ciphertext
    
    # Decrypt a number
    def decrypt_number(self, ciphertext):
        d, n = self.private_key
        # Decryption formula: M = C^d mod n
        message = pow(ciphertext, d, n)
        return message
    
    # Encrypt text
    def encrypt_text(self, text):
        print("\nEncrypting text: '" + text + "'")
        print("Converting characters to ASCII and encrypting...")
        
        encrypted = []
        for i, char in enumerate(text):
            ascii_val = ord(char)
            
            if ascii_val >= self.n:
                raise ValueError("Character ASCII value too large")
            
            encrypted_val = self.encrypt_number(ascii_val)
            print("  '" + char + "' (ASCII " + str(ascii_val) + ") -> " + str(encrypted_val))
            encrypted.append(encrypted_val)
        
        print("Text encrypted successfully!")
        return encrypted
    
    # Decrypt text
    def decrypt_text(self, encrypted_data):
        print("\nDecrypting text...")
        
        decrypted = []
        for encrypted_val in encrypted_data:
            decrypted_val = self.decrypt_number(encrypted_val)
            char = chr(decrypted_val)
            print("  " + str(encrypted_val) + " -> ASCII " + str(decrypted_val) + " ('" + char + "')")
            decrypted.append(char)
        
        result = ''.join(decrypted)
        print("Text decrypted successfully!")
        return result
    
    # Display keys
    def display_keys(self):
        e, n = self.public_key
        d, n2 = self.private_key
        
        print("\n" + "="*70)
        print("RSA KEYS")
        print("="*70)
        print("Public Key (share with anyone):")
        print("  e =", e)
        print("  n =", n)
        print("\nPrivate Key (keep secret):")
        print("  d =", d)
        print("  n =", n2)
        print("="*70)


# Display menu
def display_menu():
    print("\n" + "="*70)
    print("ASSIGNMENT 4A: RSA ON TEXT AND NUMBERS - MENU")
    print("="*70)
    print("1. Generate New RSA Keys")
    print("2. Display Current Keys")
    print("3. Encrypt a Number")
    print("4. Decrypt a Number")
    print("5. Encrypt Text")
    print("6. Decrypt Text (from last encryption)")
    print("7. Exit")
    print("="*70)


# Main function
def main():
    print("\n" + "="*70)
    print("ASSIGNMENT 4A: RSA ENCRYPTION ON TEXT AND NUMBERS")
    print("="*70)
    print("\nThis program demonstrates RSA encryption for:")
    print("- Individual numbers")
    print("- Text messages (converted to ASCII)")
    
    # Initialize RSA with 16-bit keys
    rsa = RSA(key_size=16)
    
    # Variable to store encrypted text
    encrypted_text_data = None
    original_text = None
    
    # Main menu loop
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-7): ")
        
        if choice == "1":
            # Generate new keys
            print("\n" + "-"*70)
            print("GENERATE NEW RSA KEYS")
            print("-"*70)
            
            key_size_input = input("Enter key size in bits (8, 16, or 32): ")
            try:
                key_size = int(key_size_input)
                if key_size not in [8, 16, 32]:
                    print("Invalid size! Using 16-bit.")
                    key_size = 16
                
                rsa = RSA(key_size=key_size)
                
            except ValueError:
                print("Invalid input! Keys not changed.")
        
        elif choice == "2":
            # Display keys
            rsa.display_keys()
        
        elif choice == "3":
            # Encrypt number
            print("\n" + "-"*70)
            print("ENCRYPT A NUMBER")
            print("-"*70)
            
            try:
                number = int(input("Enter a number to encrypt: "))
                
                if number >= rsa.n:
                    print("\nError: Number too large!")
                    print("Maximum value allowed:", rsa.n - 1)
                    continue
                
                print("\nOriginal number:", number)
                print("Encrypting using formula: C = M^e mod n")
                print("C = " + str(number) + "^" + str(rsa.public_key[0]) + " mod " + str(rsa.n))
                
                encrypted = rsa.encrypt_number(number)
                
                print("\nEncrypted value:", encrypted)
                print("\nYou can decrypt this using option 4")
                
            except ValueError as e:
                print("Error:", str(e))
        
        elif choice == "4":
            # Decrypt number
            print("\n" + "-"*70)
            print("DECRYPT A NUMBER")
            print("-"*70)
            
            try:
                encrypted = int(input("Enter encrypted value: "))
                
                print("\nEncrypted value:", encrypted)
                print("Decrypting using formula: M = C^d mod n")
                print("M = " + str(encrypted) + "^" + str(rsa.private_key[0]) + " mod " + str(rsa.n))
                
                decrypted = rsa.decrypt_number(encrypted)
                
                print("\nDecrypted number:", decrypted)
                
            except ValueError as e:
                print("Error:", str(e))
        
        elif choice == "5":
            # Encrypt text
            print("\n" + "-"*70)
            print("ENCRYPT TEXT")
            print("-"*70)
            
            text = input("Enter text to encrypt: ")
            
            try:
                encrypted_text_data = rsa.encrypt_text(text)
                original_text = text
                
                print("\nOriginal text: '" + text + "'")
                print("Encrypted data:", encrypted_text_data)
                print("\nUse option 6 to decrypt this text")
                
            except ValueError as e:
                print("Error:", str(e))
        
        elif choice == "6":
            # Decrypt text
            print("\n" + "-"*70)
            print("DECRYPT TEXT")
            print("-"*70)
            
            if encrypted_text_data is None:
                print("\nNo encrypted text available!")
                print("Please encrypt text first using option 5")
            else:
                print("Encrypted data:", encrypted_text_data)
                
                decrypted_text = rsa.decrypt_text(encrypted_text_data)
                
                print("\n" + "="*70)
                print("VERIFICATION")
                print("="*70)
                print("Original text:  '" + original_text + "'")
                print("Decrypted text: '" + decrypted_text + "'")
                
                if original_text == decrypted_text:
                    print("\nStatus: SUCCESS - Texts match perfectly!")
                else:
                    print("\nStatus: FAILED - Texts do not match")
                print("="*70)
        
        elif choice == "7":
            # Exit
            print("\nThank you for using RSA encryption system!")
            print("Exiting...")
            break
        
        else:
            print("\nInvalid choice! Please enter 1-7")


# Run the program
if __name__ == "__main__":
    main()