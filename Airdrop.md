Here's a summary of the flow of the script:

1. Initialization: The script starts by initializing necessary modules and constants, such as subprocess, csv, base58, json, re, and time. It also defines the base58 alphabet constant used for Dogecoin addresses.

2. Address Sanitization and Validation: Two functions are defined to sanitize Dogecoin addresses by removing non-Base58 characters and to check the validity of Dogecoin addresses.

3. Reading Addresses from CSV: Another function reads Dogecoin addresses from a CSV file, strips any extra spaces, and adds them to a list of addresses.

4. Minting NFTs for Addresses: The main function mint_nfts_for_addresses is defined, which takes a list of addresses and an HTML file path as inputs. It initializes dictionaries to store minted addresses and counts the total and remaining addresses.

5. Processing Addresses: The script iterates through each address, sanitizes it, and checks its validity. It then syncs the wallet to check for available UTXOs and continues processing if UTXOs are available.

6. Minting Process: For each valid address with available UTXOs, the script constructs and executes a mint command using subprocess. It captures the output to check for successful broadcasts and extracts the transaction ID (txid) if successful.

7. Writing to JSON File: After each successful broadcast, the script updates the minted addresses dictionary and writes it to a JSON file. It also prints the progress and status of each broadcast.

8. Main Function: The main function reads addresses from the CSV file, prints the total number of addresses, and calls the mint_nfts_for_addresses function to start the minting process.

9.Script Execution: The script is executed when the Python file is run directly (if __name__ == "__main__":), which triggers the main function.

Overall, the script reads Dogecoin addresses from a CSV file, checks their validity, syncs the wallet for available UTXOs, mints NFTs for each address with available UTXOs, updates the JSON file after each successful broadcast, and provides progress updates during the process.
