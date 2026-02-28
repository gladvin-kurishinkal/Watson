#!/usr/bin/env python3
import argparse
import zipfile
import sys
import time

def main():
    parser = argparse.ArgumentParser(description="Brute-force a ZIP file password using a numeric range.")
    parser.add_argument("zip_file", help="Path to the target ZIP file")
    parser.add_argument("max_range", type=int, help="Maximum number to check up to (inclusive)")
    parser.add_argument("-padding","--padding", action="store_true", help="Also try zero-padded numbers up to the length of max_range")
    parser.add_argument("-showall", "--showall", action="store_true", help="Display the status of each try")
    
    args = parser.parse_args()
    
    zip_filepath = args.zip_file
    max_range = args.max_range
    
    if not zipfile.is_zipfile(zip_filepath):
        print(f"Error: '{zip_filepath}' is not a valid ZIP file or does not exist.")
        sys.exit(1)
        
    print(f"Starting brute-force attack on '{zip_filepath}'")
    print(f"Numeric range: 0 to {max_range}")
    
    # Calculate the max length for zero padding if needed
    max_len = len(str(max_range))
    
    start_time = time.time()
    
    for i in range(max_range + 1):
        # We will try the plain number string
        passwords_to_try = [str(i)]
        
        # If --padding is provided, we also check zero-padded strings
        if args.padding:
            padded = str(i).zfill(max_len)
            if padded not in passwords_to_try:
                passwords_to_try.append(padded)
        
        for pwd in passwords_to_try:
            # Print current progress cleanly
            if args.showall:
                sys.stdout.write(f"TRYING PASSWORD: {pwd} ")
            else:
                sys.stdout.write(f"\rTrying password: {pwd:<{max_len}} ")
            sys.stdout.flush()
            
            try:
                with zipfile.ZipFile(zip_filepath, 'r') as zf:
                    # Test password by reading the first file in memory instead of extracting to disk
                    for zinfo in zf.infolist():
                        zf.read(zinfo, pwd=pwd.encode('utf-8'))
                        break # Successfully reading one encrypted file confirms the password
                    
                    elapsed_time = time.time() - start_time
                    if args.showall:
                        sys.stdout.write("- SUCCESS")
                    print(f"\n\n[SUCCESS] Password found: {pwd}")
                    print(f"Time taken: {elapsed_time:.2f} seconds")
                    sys.exit(0)
            except RuntimeError as e:
                # 'Bad password' or other extraction exceptions typically fall here
                if args.showall:
                    sys.stdout.write("- FAILED\n")
                    sys.stdout.flush()
            except Exception as e:
                # Ignore other exceptions like CRC bad magic which can happen if pwd is wrong
                if args.showall:
                    sys.stdout.write("- FAILED\n")
                    sys.stdout.flush()
                
    elapsed_time = time.time() - start_time
    print(f"\n\n[FAILURE] Password not found in the range 0 to {max_range}.")
    print(f"Time taken: {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    main()
