# Vigenère Cipher Cryptanalysis Notes

## 1. Objective

The objective of this experiment is to recover the key and plaintext of a Vigenère cipher using Kasiski examination, Index of Coincidence and frequency analysis.

## 2. Preprocessing

The given ciphertext was read from the dataset and preprocessed by removing spaces and special characters. All alphabetic characters were converted to uppercase.

The cleaned ciphertext length obtained was:

**395 characters**

## 3. Kasiski Examination

Repeated sequences of three to five characters were searched in the ciphertext.

Several repeated patterns were identified.

Important repeated patterns included:

* `YSZ`
* `SZW`
* `ZWX`
* `ETZ`
* `HQS`
* `QSV`
* `MJE`
* `OSD`
* `AZE`
* `ELH`
* `MUZ`

The distances between repeated occurrences included:

* 336
* 330
* 210
* 294
* 112
* 182
* 14
* 114
* 98
* 57

## 4. Factor Analysis

The factors of the repeated distances were calculated.

The factor **14** appeared for several important distances, including:

* 336
* 210
* 294
* 112
* 182
* 14
* 98

This repeated occurrence of factor 14 provided strong evidence that the key length could be 14.

Therefore, **14 was selected as the candidate key length**.

## 5. Index of Coincidence

The Index of Coincidence of the complete ciphertext was calculated as:

**0.0426**

The IC value was used as supporting evidence along with Kasiski examination.

The final estimated key length selected for further frequency analysis was:

**14**

## 6. Group Formation

The cleaned ciphertext was divided into 14 groups according to the estimated key length.

Each group contains characters encrypted using the same key position.

The groups were then analyzed independently using frequency analysis.

## 7. Frequency Analysis

Frequency analysis was performed on each of the 14 groups.

The frequency of letters A-Z was calculated separately for each group.

Each group was treated approximately as a Caesar cipher. The probable Caesar shift was determined by comparing the frequency distribution with expected English letter frequencies.

The resulting shifts produced the following key:

**AMBROISETHOMAS**

## 8. Recovered Key

The recovered Vigenère key is:

```text
AMBROISETHOMAS
```

Key length:

```text
14
```

The key positions are:

| Position | Key Letter |
| -------- | ---------- |
| 1        | A          |
| 2        | M          |
| 3        | B          |
| 4        | R          |
| 5        | O          |
| 6        | I          |
| 7        | S          |
| 8        | E          |
| 9        | T          |
| 10       | H          |
| 11       | O          |
| 12       | M          |
| 13       | A          |
| 14       | S          |

## 9. Decryption

The recovered key was repeated over the complete ciphertext and used to decrypt the message using:

`P = (C - K + 26) mod 26`

The recovered plaintext begins with:

```text
DOYOUKNOWTHELANDWHERETHEORANGETREEBLOSSOMS
```

The plaintext continues as meaningful English text and includes:

```text
THE COUNTRY OF GOLDEN FRUITS AND MARVELOUS ROSES
```

and

```text
WHERE THE BREEZE IS SOFTER AND BIRDS LIGHTER
```

The complete recovered plaintext was stored in:

`outputs/vigenere/recovered_plaintext.txt`

## 10. Verification

The recovered plaintext was re-encrypted using the recovered key:

```text
AMBROISETHOMAS
```

The generated ciphertext was compared with the original cleaned ciphertext.

The re-encryption produced the original ciphertext.

Therefore:

**Verification: SUCCESS**

## 11. Conclusion

The Vigenère ciphertext was successfully analyzed using Kasiski examination and frequency analysis.

Repeated ciphertext patterns were identified and their distances were calculated. Common factors of these distances suggested possible key lengths. Factor 14 appeared repeatedly among the important distances and was selected as the estimated key length.

The ciphertext was divided into 14 groups and frequency analysis was performed on each group. The probable shifts produced the key `AMBROISETHOMAS`.

The recovered key was used to decrypt the ciphertext and produced meaningful English plaintext. Finally, the plaintext was re-encrypted using the recovered key and the resulting ciphertext matched the original ciphertext, confirming the recovered solution.
