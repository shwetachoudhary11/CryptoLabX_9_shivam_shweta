
import random
import secrets
import string
import time




def generate_keystream(seed, length):
    """
    Generate one 8-bit keystream value per byte
    using Python's MT19937 implementation.
    """

    rng = random.Random(seed)

    keystream = bytes(
        rng.getrandbits(8) for _ in range(length)
    )

    return keystream



def encrypt_decrypt(data, seed):
    """
    The same function performs encryption and decryption.
    Both operations use XOR with the same keystream.
    """

    keystream = generate_keystream(seed, len(data))

    result = bytes(
        a ^ b for a, b in zip(data, keystream)
    )

    return result




def part_a():

    print("\n========== PART A ==========")

    original_seed = secrets.randbelow(65536)

    prefix_length = secrets.randbelow(16) + 5

    characters = string.ascii_letters + string.digits + string.punctuation

    prefix = ''.join(
        secrets.choice(characters)
        for _ in range(prefix_length)
    )

    known_pattern = "A" * 14

    plaintext = (prefix + known_pattern).encode("ascii")

    ciphertext = encrypt_decrypt(plaintext, original_seed)

    print("\nOriginal seed:", original_seed)
    print("Plaintext:", plaintext.decode("ascii"))
    print("Ciphertext (hex):", ciphertext.hex())

    decrypted = encrypt_decrypt(ciphertext, original_seed)

    print("\nDecrypted plaintext:", decrypted.decode("ascii"))

    if decrypted == plaintext:
        print("Encryption/Decryption verification: SUCCESS")
    else:
        print("Encryption/Decryption verification: FAILED")

    

    print("\nStarting seed recovery...")

    recovered_seed = None
    recovered_plaintext = None
    seeds_tested = 0

    for candidate_seed in range(65536):

        seeds_tested += 1

        candidate_plaintext = encrypt_decrypt(
            ciphertext, candidate_seed
        )

        if b"A" * 14 in candidate_plaintext:

            recovered_seed = candidate_seed
            recovered_plaintext = candidate_plaintext
            break

    print("\nSeeds tested:", seeds_tested)
    print("Recovered seed:", recovered_seed)

    if recovered_seed is not None:

        print(
            "Recovered plaintext:",
            recovered_plaintext.decode("ascii")
        )

        # Verify recovered seed against complete plaintext
        verification = encrypt_decrypt(
            ciphertext, recovered_seed
        )

        print(
            "Full plaintext verification:",
            verification == plaintext
        )

        print(
            "Known 14-character sequence found:",
            b"A" * 14 in verification
        )

        print(
            "Seed recovery verification:",
            recovered_seed == original_seed
        )

    else:
        print("No matching seed found.")




def generate_reset_token(timestamp):

    rng = random.Random(timestamp)

    token = bytes(
        rng.getrandbits(8) for _ in range(16)
    )

    return token


def part_b():

    print("\n========== PART B ==========")

    # Record current Unix timestamp
    timestamp = int(time.time())


    original_token = generate_reset_token(timestamp)

    print("\nOriginal timestamp:", timestamp)
    print("Generated token:", original_token.hex())


    start_time = timestamp - 300
    end_time = timestamp + 300

    print("\nSearching for timestamp...")
    print("Search interval:", start_time, "to", end_time)
    print("Total possible timestamps:", end_time - start_time + 1)

    recovered_timestamp = None
    candidates_tested = 0

    for candidate_timestamp in range(
        start_time, end_time + 1
    ):

        candidates_tested += 1

        candidate_token = generate_reset_token(
            candidate_timestamp
        )

        if candidate_token == original_token:

            recovered_timestamp = candidate_timestamp
            break

    print("\nCandidates tested:", candidates_tested)
    print("Recovered timestamp:", recovered_timestamp)


    if recovered_timestamp is not None:

        verification_token = generate_reset_token(
            recovered_timestamp
        )

        print(
            "Regenerated token:",
            verification_token.hex()
        )

        print(
            "Token verification:",
            verification_token == original_token
        )

        print(
            "Timestamp verification:",
            recovered_timestamp == timestamp
        )

    else:
        print("Timestamp not recovered.")


def main():

    part_a()
    part_b()


if __name__ == "__main__":
    main()
