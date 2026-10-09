# Vigenère Cipher Cryptanalysis Notes

## Objective

The objective of this experiment is to recover the key and plaintext of a Vigenère cipher using Kasiski examination, Index of Coincidence and frequency analysis.

## 1. Preprocessing

The given ciphertext was preprocessed by removing spaces and special characters. All remaining alphabetic characters were converted to uppercase.

Cleaned ciphertext length:

**________ characters**

## 2. Kasiski Examination

Repeated sequences of three to five characters were searched in the ciphertext.

The positions of repeated sequences were recorded and the distances between repeated occurrences were calculated.

The factors of these distances were then examined to identify common factors.

### Observation

Important repeated patterns:

**____________________________**

Important distances:

**____________________________**

Common factors:

**____________________________**

Based on the repeated distances, the candidate key lengths were:

**____________________________**

## 3. Index of Coincidence

The Index of Coincidence was calculated for the ciphertext and the resulting value was:

**____________________________**

The IC value was used as supporting evidence while selecting the probable key length.

## 4. Estimated Key Length

After considering the Kasiski factors and IC analysis, the estimated key length was:

**________**

## 5. Group Formation

The cleaned ciphertext was divided into groups according to the estimated key length.

Each group contains characters encrypted using the same key character.

The groups were then treated as independent Caesar-cipher groups.

## 6. Frequency Analysis

Frequency analysis was performed separately for every group.

For each group, the frequency of letters A-Z was calculated.

The frequency distributions were compared with expected English letter frequencies to estimate the Caesar shift.

## 7. Key Recovery

The probable shifts obtained from the groups were converted into letters.

The recovered key was:

**________________**

## 8. Decryption

The recovered key was applied repeatedly to the ciphertext.

The Vigenère decryption formula used was:

`P = (C - K) mod 26`

where:

* P = plaintext value
* C = ciphertext value
* K = key value

The recovered plaintext was:

**[WRITE YOUR ACTUAL RECOVERED PLAINTEXT HERE]**

## 9. Verification

The recovered plaintext was re-encrypted using the recovered key.

The generated ciphertext was compared with the original cleaned ciphertext.

Verification result:

**________________**

If both ciphertexts match exactly, the recovered key and plaintext are considered correct.

## 10. Conclusion

The Vigenère cipher was analyzed using Kasiski examination and frequency analysis. Repeated ciphertext patterns and their distances were used to estimate possible key lengths. The ciphertext was divided into groups according to the estimated key length and each group was analyzed as a Caesar cipher. The probable shifts were combined to obtain the Vigenère key. The recovered key was used to decrypt the ciphertext, and the result was verified by re-encrypting the recovered plaintext and comparing it with the original ciphertext.
