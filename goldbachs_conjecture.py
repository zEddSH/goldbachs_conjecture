# Goldbach's Conjecture is a famous conjecture that has never been proven or disproven.
# It states that every even number greater than 2 can be expressed as the sum of two prime numbers.
# It's been proven to 400_000_000_000_000

# Edit: I can see why it's been proven to 400T, it's very slow to calculate!

from joblib import Memory
from functools import wraps
from time import time
from tqdm import tqdm

# Store cached primes in a local file
memory = Memory("cachedir")


# Time functions for debugging
def time_it(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print("func:%r args:[%r, %r] took: %2.4f sec" % (f.__name__, args, kw, te - ts))
        return result

    return wrap


# Generate primes caching to disk
@memory.cache
@time_it
def generate_primes(n: int):
    sieve = [True] * n
    for i in tqdm(range(3, int(n**0.5) + 1, 2), desc="Generating Primes"):
        if sieve[i]:
            sieve[i * i :: 2 * i] = [False] * ((n - i * i - 1) // (2 * i) + 1)
    return [2] + [i for i in range(3, n, 2) if sieve[i]]


# Goldbach's Conjecture
@memory.cache
@time_it
def goldbachs_conjecture(limit: int):
    for i in tqdm(range(4, limit, 2), desc="Checking Goldbach's Conjecture"):
        for prime in primes:
            if prime > i:
                break
            if (i - prime) in primes:
                break
        else:
            print(f"Goldbach's Conjecture is false for {i}")
            return

    print(f"Goldbach's Conjecture is true for all even numbers up to {limit}")


# Run
target = 1_000_000_000
primes = generate_primes(target)
goldbachs_conjecture(target)
