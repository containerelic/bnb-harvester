"""
Address Deduplication Utility
-----------------------------
This script reads wallet addresses from 'address.txt',
removes duplicates, and saves unique addresses to 'unique_address.txt'.
"""

def main():
    # Start message
    print("BNB Harvester - Address Deduplication Tool")
    print("-" * 50)
    
    try:
        # Read addresses from file
        with open('address.txt', 'r') as file:
            addresses = [line.strip() for line in file if line.strip()]
        
        # Count original addresses
        original_count = len(addresses)
        print(f"Original address count: {original_count}")
        
        # Remove duplicates
        unique_addresses = list(dict.fromkeys(addresses))
        unique_count = len(unique_addresses)
        
        # Calculate statistics
        duplicates_removed = original_count - unique_count
        percentage = (duplicates_removed / original_count) * 100 if original_count > 0 else 0
        
        # Save unique addresses to file
        with open('unique_address.txt', 'w') as file:
            file.write('\n'.join(unique_addresses))
        
        # Print results
        print(f"Unique addresses: {unique_count}")
        print(f"Duplicates removed: {duplicates_removed} ({percentage:.2f}%)")
        print(f"Unique addresses saved to 'unique_address.txt'")
        print("-" * 50)
        
    except FileNotFoundError:
        print("Error: 'address.txt' not found!")
        print("Please create a file named 'address.txt' with wallet addresses (one per line).")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main() 