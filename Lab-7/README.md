# L6_L7_12 — Cloud Storage Tier

Lab 7: Fuzz Testing with Hypothesis

## About

This lab uses Hypothesis to fuzz storage quota parsing, compression ratio calculations, and bandwidth tier lookups. The starter functions crashed on malformed input; they now return `None` for invalid input, while the interactive program prints a clear validation message.

## Files

| File | Description |
|------|-------------|
| `processor.py` | Hardened functions and interactive demonstration |
| `test_processor.py` | Hypothesis no-crash tests and valid/invalid behavior checks |
| `requirements.txt` | Test dependencies |
| `Lab_7_Evidence.pdf` | Captured before/after test and demonstration output |

## Run

From this directory:

```powershell
python -m pip install -r requirements.txt
python processor.py
python -m pytest -q test_processor.py
```

The quota parser accepts non-negative integer amounts with `MB`, `GB`, or `TB` units. Compression metrics must be two finite, non-negative numbers separated by `:`, with a positive compressed size. Tier lookups accept descriptors beginning with `HOT`, `COL`, or `ARC`, case-insensitively.

Keep all Lab 7 work in this folder. See `Lab_7_FuzzTesting_Student_Handout.pdf` for the assignment requirements.