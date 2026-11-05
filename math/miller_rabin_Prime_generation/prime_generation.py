
import secrets
import time
from pathlib import Path


def miller_rabin(n, rounds):
    """Check whether n is probably prime using Miller-Rabin."""

    if n < 2:
        return False, []

    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]

    if n in small_primes:
        return True, []

    for p in small_primes:
        if n % p == 0:
            return False, []

    d = n - 1
    s = 0

    while d % 2 == 0:
        d //= 2
        s += 1

    bases_tested = []

    for _ in range(rounds):
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
    """Generate a probable prime of exactly 'bits' bits."""

    candidates_tested = 0

    while True:
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
    print("=== Miller-Rabin Prime Generation ===")

    while True:
        try:
            bits = int(input("Enter required bit length: "))

            if bits < 2:
                print("Bit length must be at least 2.")
                continue

            break

        except ValueError:
            print("Please enter a valid integer.")

    while True:
        try:
            rounds = int(input("Enter number of Miller-Rabin rounds: "))

            if rounds < 1:
                print("Number of rounds must be at least 1.")
                continue

            break

        except ValueError:
            print("Please enter a valid integer.")

    print("\nGenerating probable prime...")
    start_time = time.perf_counter()

    prime, candidate_count, bases = generate_prime(bits, rounds)

    execution_time = time.perf_counter() - start_time
    actual_bits = prime.bit_length()

    print("\n===== EXPERIMENTAL RESULTS =====")
    print("Assigned bit length:", bits)
    print("Generated prime candidate:", prime)
    print("Actual bit length:", actual_bits)
    print("Number of candidates tested:", candidate_count)
    print("Number of Miller-Rabin rounds:", rounds)
    print(f"Total execution time: {execution_time:.6f} seconds")

    print("\n===== VERIFICATION =====")
    print("Correct bit length:", actual_bits == bits)
    print("Candidate is odd:", prime % 2 == 1)
    print("Bases tested on final candidate:", len(bases))

    if len(bases) == rounds:
        print("Miller-Rabin verification: PASS")
    else:
        print("Miller-Rabin verification: INCOMPLETE")

    print("\nBases used for the final candidate:")
    for i, base in enumerate(bases, start=1):
        print(f"Round {i}: {base}")

    try:
        from sympy import isprime

        result = isprime(prime)
        print(
            "\nIndependent SymPy verification:",
            "PASS" if result else "FAIL"
        )

    except ImportError:
        print("\nSymPy is not installed.")
        print("Install it using: python -m pip install sympy")

    results_path = Path(__file__).resolve().parent / "results.txt"

    with open(results_path, "w", encoding="utf-8") as file:
        file.write("Miller-Rabin Prime Generation Results\n")
        file.write(f"Assigned bit length: {bits}\n")
        file.write(f"Generated prime candidate: {prime}\n")
        file.write(f"Actual bit length: {actual_bits}\n")
        file.write(f"Number of candidates tested: {candidate_count}\n")
        file.write(f"Number of Miller-Rabin rounds: {rounds}\n")
        file.write(f"Total execution time: {execution_time:.6f} seconds\n")
        file.write(f"Bases used: {bases}\n")

    print("\nResults saved to:", results_path)


if __name__ == "__main__":
    main()
