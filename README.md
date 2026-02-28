# Watson - ZIP Password Bruteforcer

A command-line tool written in Python to brute-force numeric passwords on ZIP files.

## Installation

Ensure you have Python 3 installed. The tool uses `pyzipper` to support WinZip AES encrypted files (compression method 99).

A convenience script `watson.sh` is provided which automatically sets up a Python virtual environment (`.venv`) and installs the needed dependencies from `requirements.txt`.

Make the script executable:
```bash
chmod +x watson.sh
```

## Usage

```bash
./watson.sh <zip_file> <max_range> [-padding] [-showall]
```

### Arguments

- `zip_file`: Path to the target ZIP file.
- `max_range`: The maximum number to check up to (inclusive). The tool will try passwords from `0` to this number.
- `-padding` or `--padding` *(Optional)*: Also try zero-padded numbers up to the length of `max_range`. For example, if `max_range` is 999, it will try `7`, `07`, and `007`.
- `-showall` *(Optional)*: Display the status of each password try on a new line (e.g. `TRYING PASSWORD: 42 - FAILED`).

### Example

To brute-force a ZIP file named `secret.zip` checking numbers up to `9999` and trying padded numbers (`0012`, `0123`, etc.):

```bash
./watson.sh secret.zip 9999 --padding
```

## How It Works

The tool attempts to decrypt the ZIP archive by reading its contents into memory using each pass-code in the numeric range. **It does not actually extract or save any files to your disk**; it simply confirms whether the password can successfully unlock the data. It uses `pyzipper` to support strong AES encryption and handles decryption exceptions (`RuntimeError`, `Bad password`, `CRC bad magic`, etc.) gracefully to quickly iterate over possible passwords.

