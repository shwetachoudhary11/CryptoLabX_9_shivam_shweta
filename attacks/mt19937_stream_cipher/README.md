
# Assignment 10: MT19937 Stream Cipher and Predictable Token Attack

## 1. Objective

To understand why MT19937, a statistical pseudorandom number generator,
is unsuitable for cryptographic applications.

This assignment demonstrates:

- MT19937-based toy stream cipher
- XOR encryption and decryption
- Known plaintext attack
- 16-bit seed recovery using brute force
- Predictable password reset tokens
- Timestamp-based seed recovery

## 2. Technologies Used

- Python 3
- random module
- secrets module
- string module
- time module

No external libraries are required.

## 3. Part A: MT19937 Stream Cipher

MT19937 is used to generate an 8-bit keystream value for each
plaintext byte.

Encryption:

C = P XOR K

Decryption:

P = C XOR K

Where:
- P = Plaintext
- C = Ciphertext
- K = Keystream

The same function is used for encryption and decryption.

### Known Plaintext Attack

A random printable prefix of 5-20 characters is generated,
followed by 14 consecutive A characters.

The plaintext is encrypted using a randomly selected
16-bit seed.

The attacker knows that the plaintext contains 14 consecutive
A characters, but does not know their location.

All 65,536 possible seeds are tested.

For each candidate seed:
1. Generate the keystream.
2. Decrypt the ciphertext.
3. Search for 14 consecutive A characters.
4. Recover the matching seed.
5. Verify the complete plaintext.

### Seed Search Space

2^16 = 65,536 possible seeds.

## 4. Part B: Predictable Password Reset Tokens

A simulated password reset token is generated using MT19937.

The current Unix timestamp is used as the seed.

Sixteen consecutive 8-bit outputs are generated and combined
into a 16-byte token.

The attacker knows that the token was generated within
300 seconds before or after the approximate timestamp.

Search interval:

T - 300 to T + 300

Total possible timestamps:

601

The program tests each candidate timestamp and compares
the generated token with the observed token.

The recovered timestamp is then used to regenerate the token
for verification.

## 5. Why MT19937 Is Not Cryptographically Secure

MT19937 is designed for statistical randomness, not security.

Reasons:

1. Its internal state can be reconstructed from sufficient
   observed outputs.
2. Its output is deterministic when the seed is known.
3. Small or predictable seeds can be brute-forced.
4. It is not designed to resist attackers.

Therefore, it should not be used for passwords, authentication
tokens, session IDs or security keys.

## 6. Pseudocode

### Part A: Seed Recovery

1. Generate ciphertext using a random 16-bit seed.
2. For each candidate seed from 0 to 65535:
   a. Generate the keystream.
   b. Decrypt the ciphertext.
   c. Search for 14 consecutive A characters.
3. If found, save the candidate seed.
4. Decrypt the complete ciphertext.
5. Verify the recovered plaintext.

### Part B: Token Prediction

1. Record the Unix timestamp T.
2. Generate a 16-byte token using MT19937 seeded with T.
3. Define the search interval from T-300 to T+300.
4. For each candidate timestamp:
   a. Seed MT19937 with the candidate timestamp.
   b. Generate 16 bytes.
   c. Compare the generated token with the observed token.
5. If a match is found, save the timestamp.
6. Regenerate the token and verify the result.

## 7. Experimental Results

Refer to results.txt for:
- Original seed
- Plaintext and ciphertext
- Recovered seed
- Decrypted plaintext
- Original timestamp
- Generated token
- Search interval
- Candidates tested
- Recovered timestamp
- Verification results

## 8. Conclusion

This assignment demonstrates that MT19937 is not suitable
for cryptographic applications.

A 16-bit seed can be recovered through brute force when
known plaintext is available.

Similarly, timestamp-based seeding makes password reset
tokens predictable when the generation time is known
within a sufficiently small interval.

Cryptographic applications should use secure random
number generators such as Python's secrets module.
