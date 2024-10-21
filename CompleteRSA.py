from random import sample
import os

# Function to find the prime numbers in a given limit and return 2 random prime numbers
def SieveOfEratosthenes(lower_limit, upper_limit):
    prime = [True for _ in range(upper_limit + 1)]
    p = 2
    while p * p <= upper_limit:
        # If prime[p] is not changed, then it is a prime
        if prime[p] == True:

            # Updating all multiples of p
            for i in range(p * p, upper_limit + 1, p):
                prime[i] = False
        p += 1

    # Append all primes in the limit
    primes = []
    for p in range(max(lower_limit, 3), upper_limit + 1):
        if prime[p]:
            primes.append(p)

    # Return 2 random primes from the list
    return primes


# Function to find the greatest common divisor of 2 numbers
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


# Function to generate the public and private keys
def rsa(prime_factor_1, prime_factor_2):
    modulus = prime_factor_1 * prime_factor_2 # modulus <-- the hard number to crack!

    # if N is even, then it's not a prime number
    # However, as sieve of Eratosthenes only returns odd numbers, due to the
    # range of 3 -> limit then it's not necessary to check if N is even 
    if modulus % 2 == 0:
        return ()

    # Euler’s Totient or φ(N)
    # Number of integers less than N that are coprime to N (i.e., numbers that
    # do not share any factors with N) 
    L = (prime_factor_2 - 1) * (prime_factor_1 - 1) # number of non-common factors (1, N)

    # Get the public exponent (E)
    for public_exponent in range(2, L): # between [2, L)
        # If the product of both gcd is 1, it means that L, E and N do not share
        # any common factors 
        if gcd(L, public_exponent) * gcd(modulus, public_exponent) == 1: # coprime with both L and N
            break # E is public value

    # Get the private exponent (D)
    private_exponent = 1
    while True:
        # searches for D such that (D * E) % L == 1, which satisfies the modular
        # multiplicative inverse relationship. This ensures that D is the
        # multiplicative inverse of E modulo L, which is required for
        # decryption. The conditions D != E and D != N are additional checks to
        # avoid trivial values for D. Once the correct D is found, the loop
        # breaks. 
        if (private_exponent * public_exponent % L == 1 and
                private_exponent != public_exponent and
                private_exponent != modulus):
            break # D is private value
        private_exponent += 1

    return ((public_exponent, modulus), (private_exponent, modulus))

def encrypt(plaintext, public_key):
    # Unpack the key into it's components
    key, n = public_key
    # Convert each letter in the plaintext to numbers based on the character
    # using a^b mod m 
    cipher = [pow(ord(char), key, n) for char in plaintext]
    # Return the array of bytes
    return cipher


def decrypt(ciphertext, private_key):
    # Unpack the key into its components
    key, n = private_key
    # Generate the plaintext based on the ciphertext and key using a^b mod m 
    aux = [str(pow(char, key, n)) for char in ciphertext]
    # Return the array of bytes as a string
    plain = [chr(int(char2)) for char2 in aux]
    return ''.join(plain)


if __name__ == "__main__":
    # clear the text of the cmd
    os.system('cls' if os.name == 'nt' else 'clear')

    print("==================================================================")
    rsa_keys = ()
    primes = SieveOfEratosthenes(1000, 5000)
    while not rsa_keys:
        # Select 2 random prime numbers
        # p1, p2 = sample(primes, 2)
        p1, p2 = 11, 13
        print(f"Generating RSA Keys with the prime numbers: {p1}, {p2}", end=" ... ")

        n = p1 * p2
        rsa_keys = rsa(p1, p2)
        if not rsa_keys:
            print("Failed")
        else:
            print("Success")

    print("n =", n)
    print("Public Key:", rsa_keys[0][0])
    print("Private Key:", rsa_keys[1][0])


    while True:
        print("\n==================================================================")
        print("1. Encrypt a message")
        print("2. Decrypt a message")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            plaintext = input("\nEnter a message to encrypt: ")
            encoded_message = encrypt(plaintext, rsa_keys[0])
            print("Encrypted message:", ' '.join(map(str, encoded_message)))
        elif choice == "2":
            ciphertext = input("\nEnter a message to decrypt: ")
            ciphertext = list(map(int, ciphertext.split()))
            print("Decrypted message:", decrypt(ciphertext, rsa_keys[1]))
        elif choice == "0":
            break
