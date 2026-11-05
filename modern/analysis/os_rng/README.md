# Operating-System Random Number Generator Analysis

## Aim

To evaluate operating-system random-number generation mechanisms and investigate their suitability for cryptographic applications.

## Generators Used

1. Linux `/dev/urandom`
2. OpenSSL RAND
3. Windows CNG using the .NET Cryptographic Random Number Generator API

## Project Structure

```text
os_rng/
├── generate_linux.sh
├── generate_windows.ps1
├── analyze_rng.ipynb
├── README.md
└── data/
    ├── linux_urandom.bin
    ├── openssl_random.bin
    └── windows_cng.bin
```

## Requirements

- Windows 10/11
- WSL Ubuntu
- OpenSSL
- Python 3
- Jupyter Notebook
- NumPy
- Pandas
- Matplotlib
- SciPy

## Dataset Generation

Each generator produces 1 MB (1,048,576 bytes) of random data.

### Linux and OpenSSL

Run from WSL Ubuntu:

```bash
cd analysis/os_rng
chmod +x generate_linux.sh
./generate_linux.sh
```

### Windows CNG

Run from Windows PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File analysis/os_rng/generate_windows.ps1
```

## Statistical Analysis

The Jupyter Notebook performs:

- Byte-frequency analysis
- Bit-distribution analysis
- Repeated-block detection
- Serial-correlation analysis
- Chi-square test
- Monobit test
- Runs test
- Final comparison

## Theoretical Investigation

The experiment investigates:

- Linux kernel CSPRNG
- OpenSSL DRBG
- Windows CNG
- Differences between statistical randomness and cryptographic security

## Important Observation

Passing statistical tests does not guarantee cryptographic security. Statistical tests identify certain observable patterns, whereas cryptographic security also requires unpredictability and resistance to attacks.

## How to Run the Notebook

From the repository root:

```powershell
jupyter notebook analysis/os_rng/analyze_rng.ipynb
```

Select the Python environment containing the required libraries and execute all cells.
