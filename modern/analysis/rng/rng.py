
import csv
import math
import subprocess
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chisquare


# ============================================================
# CONFIGURATION
# ============================================================

SIZE = 1024 * 1024       # 1 MiB = 1,048,576 bytes
BLOCK_SIZE = 16          # Analyze repeated 16-byte blocks
ALPHA = 0.01             # Statistical significance level

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
RESULT_DIR = BASE_DIR / "results"

DATA_DIR.mkdir(parents=True, exist_ok=True)
RESULT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# STEP 1: GENERATE DATA USING LINUX /dev/urandom
# ============================================================

def generate_linux_urandom():

    print("\n[1] Generating data using Linux /dev/urandom...")

    output_file = DATA_DIR / "linux_urandom.bin"

    # This code runs directly inside Linux/WSL.
    with open("/dev/urandom", "rb") as random_source:
        with open(output_file, "wb") as destination:

            remaining = SIZE

            while remaining > 0:
                chunk_size = min(4096, remaining)
                random_bytes = random_source.read(chunk_size)

                if not random_bytes:
                    raise RuntimeError("Unable to read from /dev/urandom")

                destination.write(random_bytes)
                remaining -= len(random_bytes)

    print("Linux data generated successfully.")
    print("File:", output_file)
    print("Size:", output_file.stat().st_size, "bytes")


# ============================================================
# STEP 2: GENERATE DATA USING OPENSSL RAND
# ============================================================

def generate_openssl():

    print("\n[2] Generating data using OpenSSL RAND...")

    output_file = DATA_DIR / "openssl_random.bin"

    try:
        subprocess.run(
            [
                "openssl",
                "rand",
                "-out",
                str(output_file),
                str(SIZE)
            ],
            check=True
        )

    except FileNotFoundError:
        raise RuntimeError(
            "OpenSSL is not installed. Run: sudo apt install openssl"
        )

    print("OpenSSL data generated successfully.")
    print("File:", output_file)
    print("Size:", output_file.stat().st_size, "bytes")


# ============================================================
# STEP 3: GENERATE DATA USING WINDOWS CNG
# ============================================================

def generate_windows_cng():

    print("\n[3] Generating data using Windows CNG...")

    output_file = DATA_DIR / "windows_cng.bin"

    if sys.platform == "win32":

        # If running directly on Windows, use the local path.
        windows_output_path = str(output_file)

    elif sys.platform.startswith("linux"):

        # Convert WSL/Linux path into a Windows path.
        try:
            result = subprocess.run(
                ["wslpath", "-w", str(output_file)],
                capture_output=True,
                text=True,
                check=True
            )

            windows_output_path = result.stdout.strip()

        except subprocess.CalledProcessError:
            raise RuntimeError("Could not convert the output path using wslpath.")

    else:
        raise RuntimeError("Unsupported operating system.")

    # Escape single quotes for PowerShell.
    windows_output_path = windows_output_path.replace("'", "''")

    # PowerShell uses .NET's cryptographic random-number API.
    # On Windows this is backed by the Windows cryptographic
    # random-number infrastructure (CNG).
    powershell_script = f"""
    $ErrorActionPreference = "Stop"

    $size = {SIZE}
    $outputFile = '{windows_output_path}'

    $rng = [System.Security.Cryptography.RandomNumberGenerator]::Create()

    try {{
        $bytes = New-Object byte[] $size
        $rng.GetBytes($bytes)
        [System.IO.File]::WriteAllBytes($outputFile, $bytes)
    }}
    finally {{
        $rng.Dispose()
    }}

    Write-Output "Windows cryptographic random data generated."
    """

    try:

        # From WSL, call Windows PowerShell.
        # From Windows Python, call PowerShell directly.
        powershell_executable = (
            "powershell.exe" if sys.platform.startswith("linux")
            else "powershell"
        )

        subprocess.run(
            [
                powershell_executable,
                "-NoProfile",
                "-NonInteractive",
                "-Command",
                powershell_script
            ],
            check=True
        )

    except FileNotFoundError:
        raise RuntimeError(
            "Windows PowerShell was not found. "
            "Check that Windows/WSL interoperability is enabled."
        )

    print("Windows CNG data generated successfully.")
    print("File:", output_file)

    if not output_file.exists():
        raise RuntimeError("Windows CNG output file was not created.")

    print("Size:", output_file.stat().st_size, "bytes")


# ============================================================
# STEP 4: BYTE FREQUENCY DISTRIBUTION
# ============================================================

def byte_frequency(data):

    counts = np.bincount(data, minlength=256)

    expected = len(data) / 256

    return counts, expected


# ============================================================
# STEP 5: BIT DISTRIBUTION
# ============================================================

def bit_distribution(data):

    bits = np.unpackbits(data)

    ones = int(np.sum(bits))
    zeros = len(bits) - ones

    zero_percentage = zeros / len(bits) * 100
    one_percentage = ones / len(bits) * 100

    return bits, zeros, ones, zero_percentage, one_percentage


# ============================================================
# STEP 6: REPEATED PATTERN ANALYSIS
# ============================================================

def repeated_patterns(data):

    blocks = [
        data[i:i + BLOCK_SIZE].tobytes()
        for i in range(0, len(data), BLOCK_SIZE)
    ]

    total_blocks = len(blocks)
    unique_blocks = len(set(blocks))

    repeated_occurrences = total_blocks - unique_blocks

    return total_blocks, unique_blocks, repeated_occurrences


# ============================================================
# STEP 7: SERIAL CORRELATION
# ============================================================

def serial_correlation(data):

    first = data[:-1].astype(np.float64)
    second = data[1:].astype(np.float64)

    correlation = np.corrcoef(first, second)[0, 1]

    return float(correlation)


# ============================================================
# STEP 8: CHI-SQUARE TEST
# ============================================================

def chi_square_test(counts, expected):

    expected_counts = np.full(256, expected)

    statistic, p_value = chisquare(
        counts,
        f_exp=expected_counts
    )

    decision = (
        "Reject H0"
        if p_value < ALPHA
        else "Do not reject H0"
    )

    return float(statistic), float(p_value), decision


# ============================================================
# STEP 9: MONOBIT TEST
# ============================================================

def monobit_test(bits, zeros, ones):

    n = len(bits)

    # Difference between the number of ones and zeros.
    total = ones - zeros

    z_value = abs(total) / math.sqrt(n)

    # Two-sided normal approximation.
    p_value = math.erfc(z_value / math.sqrt(2))

    decision = (
        "Reject H0"
        if p_value < ALPHA
        else "Do not reject H0"
    )

    return z_value, p_value, decision


# ============================================================
# STEP 10: RUNS TEST
# ============================================================

def runs_test(bits, zeros, ones):

    n = len(bits)

    proportion_ones = ones / n

    # Runs test prerequisite.
    applicable = (
        abs(proportion_ones - 0.5) < 2 / math.sqrt(n)
    )

    if not applicable:
        return None, None, "Not applicable: prerequisite failed"

    # Count transitions between consecutive bits.
    runs = 1 + int(np.sum(bits[1:] != bits[:-1]))

    expected_runs = 1 + (2 * zeros * ones / n)

    variance = (
        2 * zeros * ones * (2 * zeros * ones - n)
        / (n ** 2 * (n - 1))
    )

    if variance <= 0:
        return runs, None, "Not applicable: invalid variance"

    z_value = abs(runs - expected_runs) / math.sqrt(variance)

    p_value = math.erfc(z_value / math.sqrt(2))

    decision = (
        "Reject H0"
        if p_value < ALPHA
        else "Do not reject H0"
    )

    return runs, p_value, decision


# ============================================================
# STEP 11: ANALYZE ONE DATASET
# ============================================================

def analyze_dataset(name, file_path):

    print("\n" + "=" * 65)
    print("ANALYSIS:", name)
    print("=" * 65)

    raw = file_path.read_bytes()

    if len(raw) != SIZE:
        raise ValueError(
            f"{file_path.name} must contain exactly {SIZE} bytes."
        )

    data = np.frombuffer(raw, dtype=np.uint8)

    # 1. Byte frequency
    counts, expected = byte_frequency(data)

    # 2. Bit distribution
    bits, zeros, ones, zero_pct, one_pct = bit_distribution(data)

    # 3. Repeated patterns
    total_blocks, unique_blocks, repeated = repeated_patterns(data)

    # 4. Serial correlation
    correlation = serial_correlation(data)

    # 5. Chi-square test
    chi_stat, chi_p, chi_decision = chi_square_test(
        counts, expected
    )

    # 6. Monobit test
    mono_z, mono_p, mono_decision = monobit_test(
        bits, zeros, ones
    )

    # 7. Runs test
    runs, runs_p, runs_decision = runs_test(
        bits, zeros, ones
    )

    # Display results.
    print("File size:", len(data), "bytes")
    print("Expected frequency per byte:", expected)

    print("\nBIT DISTRIBUTION")
    print("Zeros:", zeros)
    print("Ones:", ones)
    print("Zero percentage:", round(zero_pct, 4), "%")
    print("One percentage:", round(one_pct, 4), "%")

    print("\nREPEATED PATTERNS")
    print("Total blocks:", total_blocks)
    print("Unique blocks:", unique_blocks)
    print("Repeated occurrences:", repeated)

    print("\nSERIAL CORRELATION")
    print("Correlation coefficient:", correlation)

    print("\nCHI-SQUARE TEST")
    print("Statistic:", chi_stat)
    print("P-value:", chi_p)
    print("Decision:", chi_decision)

    print("\nMONOBIT TEST")
    print("Z value:", mono_z)
    print("P-value:", mono_p)
    print("Decision:", mono_decision)

    print("\nRUNS TEST")
    print("Number of runs:", runs)
    print("P-value:", runs_p)
    print("Decision:", runs_decision)

    # Save byte frequency CSV.
    frequency_file = (
        RESULT_DIR /
        (name.replace(" ", "_").replace("/", "_")
         + "_byte_frequency.csv")
    )

    with open(frequency_file, "w", newline="") as csvfile:

        writer = csv.writer(csvfile)

        writer.writerow([
            "Byte Value",
            "Observed Frequency",
            "Expected Frequency"
        ])

        for value in range(256):
            writer.writerow([
                value,
                int(counts[value]),
                expected
            ])

    return {
        "Source": name,
        "File Size (bytes)": len(data),
        "Zeros": zeros,
        "Ones": ones,
        "Zero (%)": zero_pct,
        "One (%)": one_pct,
        "Total Blocks": total_blocks,
        "Unique Blocks": unique_blocks,
        "Repeated Occurrences": repeated,
        "Serial Correlation": correlation,
        "Chi-square Statistic": chi_stat,
        "Chi-square P-value": chi_p,
        "Chi-square Decision": chi_decision,
        "Monobit Z": mono_z,
        "Monobit P-value": mono_p,
        "Monobit Decision": mono_decision,
        "Runs": runs,
        "Runs P-value": runs_p,
        "Runs Decision": runs_decision
    }, counts, expected


# ============================================================
# STEP 12: GENERATE BYTE FREQUENCY GRAPH
# ============================================================

def generate_graphs(graph_data):

    print("\nGenerating byte-frequency graph...")

    fig, axes = plt.subplots(3, 1, figsize=(13, 12))

    for ax, (name, counts, expected) in zip(axes, graph_data):

        ax.bar(range(256), counts, width=1.0)

        ax.axhline(
            y=expected,
            linestyle="--",
            label="Expected frequency"
        )

        ax.set_title(name)
        ax.set_xlabel("Byte value (0-255)")
        ax.set_ylabel("Frequency")
        ax.legend()

    plt.tight_layout()

    graph_file = RESULT_DIR / "byte_frequency_comparison.png"

    plt.savefig(graph_file, dpi=300)
    plt.close()

    print("Graph saved:", graph_file)


# ============================================================
# STEP 13: SAVE FINAL COMPARISON CSV
# ============================================================

def save_summary(summary):

    output_file = RESULT_DIR / "final_results.csv"

    with open(output_file, "w", newline="") as csvfile:

        writer = csv.DictWriter(
            csvfile,
            fieldnames=summary[0].keys()
        )

        writer.writeheader()
        writer.writerows(summary)

    print("\nFinal comparison saved:", output_file)


# ============================================================
# MAIN FUNCTION
# ============================================================

def main():

    print("=" * 65)
    print("OPERATING SYSTEM RANDOM NUMBER GENERATOR ANALYSIS")
    print("=" * 65)

    print("\nRunning platform:", sys.platform)
    print("Data size:", SIZE, "bytes")
    print("Significance level:", ALPHA)

    if not sys.platform.startswith("linux") and sys.platform != "win32":
        raise RuntimeError("Run this program on Windows or Linux/WSL.")

    # Generate datasets.
    if sys.platform.startswith("linux"):
        generate_linux_urandom()
        generate_openssl()
        generate_windows_cng()

    else:
        raise RuntimeError(
            "This version is designed to run from WSL Ubuntu. "
            "Run it inside WSL so it can generate all three datasets."
        )

    # Analyze datasets.
    files = [
        ("Linux /dev/urandom", DATA_DIR / "linux_urandom.bin"),
        ("OpenSSL RAND", DATA_DIR / "openssl_random.bin"),
        ("Windows CNG", DATA_DIR / "windows_cng.bin")
    ]

    summary = []
    graph_data = []

    for name, file_path in files:

        result, counts, expected = analyze_dataset(
            name, file_path
        )

        summary.append(result)
        graph_data.append((name, counts, expected))

    # Save final outputs.
    generate_graphs(graph_data)
    save_summary(summary)

    print("\n" + "=" * 65)
    print("ASSIGNMENT EXECUTION COMPLETED")
    print("=" * 65)

    print("\nGenerated data files:")
    print("1. linux_urandom.bin")
    print("2. openssl_random.bin")
    print("3. windows_cng.bin")

    print("\nGenerated result files:")
    print("1. final_results.csv")
    print("2. byte_frequency_comparison.png")
    print("3. Individual byte-frequency CSV files")

    print("\nAll files are stored in:")
    print(BASE_DIR)


if __name__ == "__main__":
    main()
