# Watson - ZIP Password Bruteforcer

A command-line tool written in Python to brute-force numeric passwords on ZIP files.

## Installation

Ensure you have Python 3 installed. You can run the program directly without installing any third-party dependencies.

Make the script executable (if it isn't already):
```bash
chmod +x watson.py
```

## Usage

```bash
./watson.py <zip_file> <max_range> [-padding] [-showall]
```

### Arguments

- `zip_file`: Path to the target ZIP file.
- `max_range`: The maximum number to check up to (inclusive). The tool will try passwords from `0` to this number.
- `-padding` or `--padding` *(Optional)*: Also try zero-padded numbers up to the length of `max_range`. For example, if `max_range` is 999, it will try `7`, `07`, and `007`.
- `-showall` *(Optional)*: Display the status of each password try on a new line (e.g. `TRYING PASSWORD: 42 - FAILED`).

### Example

To brute-force a ZIP file named `secret.zip` checking numbers up to `9999` and trying padded numbers (`0012`, `0123`, etc.):

```bash
./watson.py secret.zip 9999 -padding
```

## How It Works

The tool attempts to decrypt the ZIP archive by reading its contents into memory using each pass-code in the numeric range. **It does not actually extract or save any files to your disk**; it simply confirms whether the password can successfully unlock the data. It handles decryption exceptions (`RuntimeError`, `Bad password`, `CRC bad magic`, etc.) gracefully to quickly iterate over possible passwords.

