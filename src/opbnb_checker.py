from web3 import Web3
import time

# Connect to opBNB mainnet
print("Connecting to opBNB mainnet...")
opbnb = Web3(Web3.HTTPProvider('https://opbnb-mainnet-rpc.bnbchain.org'))

# Check connection
if opbnb.is_connected():
    print("Connected to opBNB mainnet!")
else:
    print("Failed to connect to opBNB mainnet!")
    exit(1)

# Transaction fee estimate based on real transaction data
FEE = 0.0000002  # Default fee in BNB (based on actual opBNB transaction data)

# Read wallet addresses from file
print("Reading wallet addresses...")
try:
    with open('unique_address.txt', 'r') as file:
        addresses = [line.strip() for line in file if line.strip()]
    print(f"Total {len(addresses)} addresses loaded.")
except FileNotFoundError:
    print("Error: unique_address.txt not found!")
    print("Please create a file named 'unique_address.txt' with one wallet address per line.")
    exit(1)

# Initialize counters
total_bnb = 0
empty_wallets = 0
wallets_with_balance = 0
total_after_fee = 0

print("\nChecking opBNB balances...")
print("-" * 70)

# Check each wallet balance
for address in addresses:
    try:
        # Validate address format
        if not Web3.is_address(address):
            print(f"Invalid address format: {address}")
            continue
            
        # Check balance
        balance_wei = opbnb.eth.get_balance(address)
        balance_bnb = balance_wei / 10**18
        
        # Calculate balance after fee
        balance_after_fee = max(0, balance_bnb - FEE)
        
        # Update totals
        total_bnb += balance_bnb
        
        # Print balance info
        if balance_bnb > 0:
            wallets_with_balance += 1
            if balance_bnb > FEE:
                total_after_fee += balance_after_fee
                print(f"{address}: {balance_bnb:.12f} BNB (After fee: {balance_after_fee:.12f} BNB)")
            else:
                print(f"{address}: {balance_bnb:.12f} BNB (Insufficient for transfer - below fee)")
        else:
            empty_wallets += 1
            
    except Exception as e:
        print(f"Error checking {address}: {str(e)}")

# Print summary
print("\n" + "=" * 70)
print(f"Total addresses checked: {len(addresses)}")
print(f"Wallets with balance: {wallets_with_balance}")
print(f"Empty wallets: {empty_wallets}")
print(f"Total BNB found: {total_bnb:.12f} BNB")
print(f"Total transferable BNB (after fees): {total_after_fee:.12f} BNB")
print(f"Estimated gas fee per transfer: {FEE:.12f} BNB")
print("=" * 70) 