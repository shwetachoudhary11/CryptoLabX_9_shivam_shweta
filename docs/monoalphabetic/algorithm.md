# Vigenère Cipher Cryptanalysis Algorithm

## Aim

To cryptanalyse a Vigenère cipher using Kasiski examination, Index of Coincidence and frequency analysis, recover the probable key and plaintext, and verify the recovered solution by re-encryption.

## Algorithm

### 1. Preprocessing

1. Read the given ciphertext from the input file.
2. Remove spaces and special characters.
3. Convert all alphabetic characters to uppercase.
4. Store the cleaned ciphertext.

### 2. Find Repeated Patterns

1. Search the ciphertext for repeated sequences of length 3 to 5.
2. Record the starting position of each repeated sequence.
3. Identify repeated sequences occurring at different positions.

### 3. Calculate Distances

1. For every repeated pattern, calculate the distance between its occurrences.
2. Store the obtained distances.
3. These distances are used to identify possible key lengths.

### 4. Find Factors

1. Find the factors of every repeated-pattern distance.
2. Compare the factors obtained from different distances.
3. Factors occurring frequently are considered possible key lengths.

### 5. Kasiski Analysis

1. Examine the repeated patterns and their distances.
2. Identify common factors among the distances.
3. Generate candidate key lengths.
4. In this experiment, key length **14** was selected because 14 occurs as a factor of several important repeated-pattern distances.

### 6. Index of Coincidence

1. Calculate the Index of Coincidence of the ciphertext.
2. Calculate IC values for groups corresponding to candidate key lengths.
3. Use IC as supporting evidence for selecting the key length.
4. For this experiment, the selected key length was **14**.

### 7. Split the Ciphertext

1. Divide the ciphertext into 14 groups.
2. Characters having the same position modulo 14 are placed in the same group.
3. Each group corresponds to one character of the Vigenère key.

### 8. Frequency Analysis

1. Calculate the frequency of A-Z in each group.
2. Treat each group approximately as a Caesar cipher.
3. Compare the frequency distribution with normal English letter frequencies.
4. Determine the most probable shift for every group.

### 9. Recover the Key

1. Determine the probable Caesar shift for every group.
2. Convert each shift into its corresponding alphabetic character.
3. Combine the characters in group order.
4. The recovered key for this experiment is:

`AMBROISETHOMAS`

### 10. Decryption

1. Repeat the recovered key over the ciphertext.
2. Convert ciphertext and key letters into numerical values from 0 to 25.
3. Apply the Vigenère decryption formula:

`P = (C - K + 26) mod 26`

4. Convert the resulting values back to letters.
5. Obtain the recovered plaintext.

### 11. Verification

1. Take the recovered plaintext.
2. Encrypt it again using the recovered key.
3. Compare the generated ciphertext with the original cleaned ciphertext.
4. If both are identical, the recovered key and plaintext are verified.
