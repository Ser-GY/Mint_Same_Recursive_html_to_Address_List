import subprocess
import csv
import os
import base58
import json
import re
import time

# Base58 alphabet constant
BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def sanitize_address(address):
    """
    Sanitizes a Dogecoin address by removing non-Base58 characters.

    Args:
    address (str): Dogecoin address to sanitize.

    Returns:
    str: Sanitized Dogecoin address.
    """
    sanitized_address = ''.join(c for c in address if c in BASE58_ALPHABET)
    return sanitized_address

def is_valid_doge_address(address):
    """
    Checks if a Dogecoin address is valid.

    Args:
    address (str): Dogecoin address to validate.

    Returns:
    bool: True if the address is valid, False otherwise.
    """
    try:
        base58.b58decode_check(address)
        return True
    except Exception:
        return False

def read_doge_addresses_from_csv(csv_file_path):
    """
    Reads Dogecoin addresses from a CSV file.

    Args:
    csv_file_path (str): Path to the CSV file containing Dogecoin addresses.

    Returns:
    list: List of Dogecoin addresses read from the CSV file.
    """
    addresses = []
    try:
        with open(csv_file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                for address in row:
                    address = address.strip()
                    if address:
                        addresses.append(address)
    except Exception as e:
        print("Error reading CSV file:", e)
        return []  # Return an empty list if there's an error reading the file
    return addresses

def mint_nfts_for_addresses(addresses, html_path):
    minted_addresses = {}
    total_addresses = len(addresses)
    addresses_left = total_addresses

    for address in addresses:
        sanitized_address = sanitize_address(address)
        if not is_valid_doge_address(sanitized_address):
            print("Invalid Dogecoin address:", address)
            continue

        # Sync wallet to check for available UTXOs
        sync_command = "node . wallet sync"
        result_sync = subprocess.run(sync_command, shell=True, capture_output=True, text=True)
        print("Output from sync command:")
        print(result_sync.stdout)

        if result_sync.stderr:
            print("Error in sync command:")
            print(result_sync.stderr)
            continue

        # Check if there are available UTXOs
        utxo_count = 0
        utxo_search = re.search(r"Total UTXOs: (\d+)", result_sync.stdout)
        if utxo_search:
            utxo_count = int(utxo_search.group(1))
            print(f"Total UTXOs: {utxo_count}")

        if utxo_count == 0:
            print("No UTXOs ready for broadcast, waiting...")
            time.sleep(30)
            continue

        # Construct and execute the mint command using subprocess
        mint_command = f"node . mint {sanitized_address} {html_path}"
        try:
            result_mint = subprocess.run(mint_command, shell=True, capture_output=True, text=True)
            print("Output from mint command:")
            print(result_mint.stdout)

            if result_mint.stderr:
                print("Error in mint command:")
                print(result_mint.stderr)
            else:
                txid_search = re.search("inscription txid: (\w+)", result_mint.stdout)
                if txid_search:
                    txid = txid_search.group(1)
                    minted_addresses[sanitized_address] = txid
                    addresses_left -= 1  # Decrease addresses left after successful broadcast
                    print(f"Transaction broadcast successful. Addresses left: {addresses_left}/{total_addresses}")
                else:
                    print("Failed to extract txid from mint command output.")
        except Exception as e:
            print("Error executing mint command:", e)

        # Check if broadcast failed
        if "broadcast failed" in result_mint.stdout:
            print("Broadcast failed, sleeping for 30 seconds...")
            time.sleep(30)

    # Write minted addresses to JSON file after all addresses processed
    with open('minted_addresses.json', 'w') as json_file:
        json.dump(minted_addresses, json_file, indent=4)
        print("Minted addresses saved to 'minted_addresses.json'.")

    # Print minted addresses for debugging
    print("Minted Addresses:")
    print(minted_addresses)

def main():
    # Configuration
    csv_file_path = '/root/shibes05/Airdrop/Airdrop.csv'  # CSV file path
    addresses = read_doge_addresses_from_csv(csv_file_path)

    # Print the number of addresses
    total_addresses = len(addresses)
    print(f"Total Dogecoin addresses to process: {total_addresses}")

    html_path = '/root/shibes05/Airdrop/Airdrop.html'  # HTML file path

    mint_nfts_for_addresses(addresses, html_path)

if __name__ == "__main__":
    main()
