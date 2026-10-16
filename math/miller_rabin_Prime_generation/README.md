
# Cryptographic Prime Generation Using Miller-Rabin

## Aim

To generate a probable prime number of exactly 512-bit length
using the Miller-Rabin probabilistic primality test.

## Theory

Miller-Rabin is a probabilistic primality testing algorithm
used to determine whether an integer is prime or composite.

For an odd integer n, express:

n - 1 = d * 2^s

where d is odd.

For each round, choose a random base a and calculate:

x = a^d mod n

If x equals 1 or n-1, the candidate passes that round.

Otherwise, repeatedly square x modulo n. If the result
becomes n-1, the round passes. If it never becomes n-1,
the candidate is composite.

A candidate that passes all selected rounds is considered
a probable prime.

## Algorithm

1. Select the required bit length (512 bits).
2. Generate a random integer of that bit length.
3. Set its least significant bit to 1 to make it odd.
4. Apply the Miller-Rabin primality test.
5. If the candidate fails, generate another candidate.
6. Repeat until a candidate passes all rounds.
7. Verify the actual bit length.
8. Verify the result independently using SymPy.
9. Record the execution time and experimental results.

## Execution

Install SymPy:

python -m pip install sympy

Run from the CryptoLabX project root:

python math/miller_rabin_prime_generation/prime_generation.py

## Experimental Results

| Parameter | Value |
|---|---|
| Assigned bit length | 512 |
| Generated prime candidate | Record program output |
| Actual bit length | 512 |
| Number of candidates tested | Record program output |
| Miller-Rabin rounds | 40 |
| Total execution time | Record program output |

## Verification

1. The generated number has exactly 512 bits.
2. The generated number is odd.
3. The candidate passes all 40 Miller-Rabin rounds.
4. SymPy's isprime() function is used as an independent check.

## Conclusion

A probable prime of the required bit length is generated
using the Miller-Rabin primality test. Its bit length,
test results, candidate count, and execution time are recorded.
An independent primality check provides additional verification.
