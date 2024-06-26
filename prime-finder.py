from random import sample
import timeit


# Function to find the prime numbers in a given limit and return 2 random prime numbers
def SieveOfEratosthenes(limit):
    prime = [True for i in range(limit + 1)]
    p = 2
    while p * p <= limit:
        # If prime[p] is not changed, then it is a prime
        if prime[p] == True:

            # Updating all multiples of p
            for i in range(p * p, limit + 1, p):
                prime[i] = False
        p += 1

    # Append all primes in the limit
    primes = []
    for p in range(2, limit + 1):
        if prime[p]:
            primes.append(p)

    # Return 2 random primes from the list
    return sample(primes, 2)


# Function to find the prime factors of a number
def get_prime_factors(n):
    # Get a g that is less than n
    for g in range(2, n):
        # Check whether g shares a factor with n
        if n % g == 0:
            continue

        # Get a g to the power of r that is equals to mN+1, where m is a constant and N is the number we are testing
        # Test all g's to the power of r until we find one that satisfies the condition of being one more than a multiple of N and
        # having an even r
        r = 1
        while (g**r) % n != 1 or r % 2 == 1:
            r += 1

        # Find the two factos that are equals to mN from g^r = mN+1
        f1 = g ** (r // 2) + 1
        f2 = g ** (r // 2) - 1

        # Use Euclid's algorithm to find the greatest common divisor of f1 and n
        # To do this, we will be dividing f1 by n until the remainder is 0, if it's still not 0, we will swap the values of f1 and n
        # and repeat the process
        # For example:
        # 32,769 / 77 = 425 R 44
        # 77 / 44 = 1 R 33
        # 44 / 33 = 1 R 11
        # 33 / 11 = 3 R 0 (The remainder is 0, so the greatest common divisor is 11)
        m = n
        while f1 % m != 0:
            # Swap the values of f1 and n
            # f1 takes the value of the divisor
            # m takes the value of the remainder
            f1, m = m, f1 % m

        # m is the greates common divisor, thus it is the first prime factor of n
        f1 = m

        # Get the other prime factor by dividing n by the greatest common divisor
        f2 = n // f1

        return f1, f2


# Function to run a single test
def run_test(silent=False, prime_limit=1000):
    start = timeit.default_timer()
    p1, p2 = SieveOfEratosthenes(prime_limit)
    n = p1 * p2
    f1, f2 = get_prime_factors(n)
    if not silent:
        print("==================================================================")
        print(f"n = {n}")
        print(f"\tFactores originales: {p1} y {p2}\n\t{p1} * {p2} = {p1 * p2}")
        print(f"\n\tFactores encontrados: {f1} y {f2}\n\t{f1} * {f2} = {f1 * f2}")
    elapsed_time = timeit.default_timer() - start
    print(f"Elapsed time: {elapsed_time} seconds") if not silent else None
    return elapsed_time


tests = 5
total_elapsed_time = 0
prime_limit = 1000
for _ in range(tests):
    total_elapsed_time += run_test(silent=True, prime_limit=prime_limit)

print(f"Average elapsed time: {total_elapsed_time / tests} seconds")
