
import secrets
import time
import argparse


def miller_rabin(n, rounds=40):
    """Test whether n is probably prime using Miller-Rabin."""

    if n < 2:
        return False, []

    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]

    if n in small_primes:
        return True, []

    for p in small_primes:
        if n % p == 0:
            return False, []

    # Write n - 1 as d * 2^s
    d = n - 1
    s = 0

    while d % 2 == 0:
        d //= 2
        s += 1

    bases_tested = []

    for _ in range(rounds):
        # Select a random base between 2 and n-2
        a = 2 + secrets.randbelow(n - 3)
        bases_tested.append(a)

        x = pow(a, d, n)

        if x == 1 or x == n - 1:
            continue

        for _ in range(s - 1):
            x = pow(x, 2, n)

            if x == n - 1:
                break
        else:
            return False, bases_tested

    return True, bases_tested


def generate_prime(bits, rounds):
    """Generate a probable prime of exactly the requested bit length."""

    candidates_tested = 0

    while True:
        # Set the highest bit to guarantee bit length
        # Set the lowest bit to guarantee an odd number
        candidate = (
            secrets.randbits(bits)
            | (1 << (bits - 1))
            | 1
        )

        candidates_tested += 1

        is_prime, bases = miller_rabin(candidate, rounds)

        if is_prime:
            return candidate, candidates_tested, bases


def main():
    parser = argparse.ArgumentParser(
        description="Cryptographic Prime Generation using Miller-Rabin"
    )

    parser.add_argument(
        "--bits",
        type=int,
        default=512,
        help="Required prime bit length"
    )

    parser.add_argument(
        "--rounds",
        type=int,
        default=40,
        help="Number of Miller-Rabin rounds"
    )

    args = parser.parse_args()

    if args.bits < 2:
        parser.error("Bit length must be at least 2")

    if args.rounds < 1:
        parser.error("Number of rounds must be at least 1")

    start_time = time.perf_counter()

    prime, candidate_count, bases = generate_prime(
        args.bits, args.rounds
    )

    end_time = time.perf_counter()
    execution_time = end_time - start_time

    actual_bits = prime.bit_length()

    print("\n===== MILLER-RABIN PRIME GENERATION =====")
    print("Assigned bit length:", args.bits)
    print("Generated prime candidate:", prime)
    print("Actual bit length:", actual_bits)
    print("Number of candidates tested:", candidate_count)
    print("Number of Miller-Rabin rounds:", args.rounds)
    print("Total execution time: {:.6f} seconds".format(
        execution_time
    ))

    print("\n===== VERIFICATION =====")
    print("Correct bit length:", actual_bits == args.bits)
    print("Candidate is odd:", prime % 2 == 1)
    print("Miller-Rabin bases tested:", len(bases))

    if len(bases) == args.rounds:
        print("Miller-Rabin verification: PASS")
    else:
        print("Miller-Rabin verification: INCOMPLETE")

    print("\nBases used for the final candidate:")
    for i, base in enumerate(bases, start=1):
        print(f"Round {i}: {base}")

    # Independent verification using SymPy
    try:
        from sympy import isprime

        result = isprime(prime)

        print("\nIndependent SymPy verification:",
              "PASS" if result else "FAIL")

    except ImportError:
        print("\nSymPy is not installed.")
        print("Install it using: python -m pip install sympy")

    # Save experimental results
    from pathlib import Path

    results_path = Path(__file__).resolve().parent / "results.txt"

    with open(results_path, "w", encoding="utf-8") as file:
        file.write("Cryptographic Prime Generation Using Miller-Rabin\n")
        file.write(f"Assigned bit length: {args.bits}\n")
        file.write(f"Generated prime candidate: {prime}\n")
        file.write(f"Actual bit length: {actual_bits}\n")
        file.write(f"Number of candidates tested: {candidate_count}\n")
        file.write(f"Number of Miller-Rabin rounds: {args.rounds}\n")
        file.write(f"Total execution time: {execution_time:.6f} seconds\n")
        file.write(f"Bases used: {bases}\n")

    print("\nResults saved to:", results_path)


if __name__ == "__main__":
    main()
