

from oracle import encrypt_message, create_padding_oracle

BLOCK_SIZE = 16


def padding_oracle_attack(iv, ciphertext, oracle):
    query_count = 0
    plaintext = bytearray()

    blocks = [
        ciphertext[i:i + BLOCK_SIZE]
        for i in range(0, len(ciphertext), BLOCK_SIZE)
    ]

    for block_index, target in enumerate(blocks):
        previous = iv if block_index == 0 else blocks[block_index - 1]
        intermediate = [0] * BLOCK_SIZE

        for pos in range(BLOCK_SIZE - 1, -1, -1):
            pad_value = BLOCK_SIZE - pos
            crafted = bytearray(BLOCK_SIZE)

            for j in range(pos + 1, BLOCK_SIZE):
                crafted[j] = intermediate[j] ^ pad_value

            found = False

            for guess in range(256):
                crafted[pos] = guess
                query_count += 1

                if not oracle(bytes(crafted), target):
                    continue

                if pos > 0:
                    check = bytearray(crafted)
                    check[pos - 1] ^= 1
                    query_count += 1

                    if not oracle(bytes(check), target):
                        continue

                intermediate[pos] = guess ^ pad_value
                found = True
                break

            if not found:
                raise RuntimeError(
                    f"Could not recover byte {pos} in block {block_index}"
                )

        plaintext_block = bytes(
            intermediate[i] ^ previous[i]
            for i in range(BLOCK_SIZE)
        )

        plaintext.extend(plaintext_block)

    padding_length = plaintext[-1]

    if not 1 <= padding_length <= BLOCK_SIZE:
        raise ValueError("Invalid recovered padding")

    if plaintext[-padding_length:] != bytes([padding_length]) * padding_length:
        raise ValueError("Recovered padding verification failed")

    return bytes(plaintext[:-padding_length]), query_count


if __name__ == "__main__":
    message = b"hello"

    key, iv, ciphertext = encrypt_message(message)
    oracle = create_padding_oracle(key)

    recovered, queries = padding_oracle_attack(
        iv, ciphertext, oracle
    )

    print("Ciphertext:", ciphertext.hex())
    print("IV:", iv.hex())
    print("Recovered plaintext:", recovered.decode("utf-8"))
    print("Total oracle queries:", queries)
    print("Recovery successful:", recovered == message)
