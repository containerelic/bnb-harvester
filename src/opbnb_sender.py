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

# Target wallet address (where to consolidate all BNB)
TARGET_WALLET = "0xb72e9223dF0A6c247D6C2b955c3654eF28d0A32B"  # Replace with your target wallet

# Gas settings - based on actual opBNB transaction data
GAS_PRICE = opbnb.to_wei('0.001', 'gwei')  # 0.001 Gwei = 0.000000000001 BNB
GAS_LIMIT = 30000  # Standard transfer uses ~28,075 gas
SAFETY_MARGIN = 200000000000  # ~0.0000002 BNB, additional safety margin

# Read private keys from file
try:
    with open('private_keys.txt', 'r') as file:
        private_keys = [line.strip() for line in file if line.strip()]
    print(f"Loaded {len(private_keys)} private keys.")
except FileNotFoundError:
    print("Error: private_keys.txt not found!")
    print("Please create a file named 'private_keys.txt' with one private key per line.")
    exit(1)

# Initialize counters
success_count = 0
failed_count = 0
total_sent = 0

print(f"\nSending BNB from {len(private_keys)} wallets to {TARGET_WALLET}...\n")

# Process each wallet
for private_key in private_keys:
    try:
        # Create account from private key
        account = opbnb.eth.account.from_key(private_key)
        from_address = account.address
        
        # Check account balance
        balance = opbnb.eth.get_balance(from_address)
        balance_bnb = balance / (10**18)
        
        # Calculate gas fee
        base_gas_fee = GAS_LIMIT * GAS_PRICE
        total_fee = base_gas_fee + SAFETY_MARGIN
        
        print(f"Wallet {from_address} balance: {balance_bnb:.12f} BNB")
        print(f"Estimated fee: {total_fee / (10**18):.12f} BNB (Base: {base_gas_fee / (10**18):.12f} + Margin: {SAFETY_MARGIN / (10**18):.12f})")
        
        # Calculate amount to send (total balance - fee)
        amount_to_send = balance - total_fee
        
        # Send only if amount is positive
        if amount_to_send > 0:
            # Create transaction
            tx = {
                'nonce': opbnb.eth.get_transaction_count(from_address),
                'to': TARGET_WALLET,
                'value': amount_to_send,
                'gas': GAS_LIMIT,
                'gasPrice': GAS_PRICE,
                'chainId': 204  # opBNB mainnet chain ID
            }
            
            # Sign transaction
            signed_tx = opbnb.eth.account.sign_transaction(tx, private_key)
            
            # Send transaction
            try:
                # For newer web3.py versions
                tx_hash = opbnb.eth.send_raw_transaction(signed_tx.raw_transaction)
            except AttributeError:
                # For older web3.py versions
                tx_hash = opbnb.eth.send_raw_transaction(signed_tx.rawTransaction)
            
            tx_hash_hex = tx_hash.hex()
            amount_to_send_bnb = amount_to_send / (10**18)
            total_sent += amount_to_send_bnb
            
            print(f"Transaction successful: {amount_to_send_bnb:.12f} BNB")
            print(f"Transaction hash: {tx_hash_hex}")
            print(f"opBNB Explorer: https://opbnb.bscscan.com/tx/{tx_hash_hex}")
            print("-" * 70)
            
            success_count += 1
            
            # Add delay between transactions - opBNB has fast confirmation times
            time.sleep(1)
        else:
            print(f"Insufficient balance - Required fee ({total_fee / (10**18):.12f} BNB) exceeds balance ({balance_bnb:.12f} BNB)")
            print("-" * 70)
            failed_count += 1
            
    except Exception as e:
        print(f"Error: {str(e)}")
        print(f"Wallet address: {from_address if 'from_address' in locals() else 'Unknown'}")
        print("-" * 70)
        failed_count += 1

# Print summary
print("\n" + "="*70)
print(f"Transactions completed: {success_count}")
print(f"Failed: {failed_count}")
print(f"Total BNB sent: {total_sent:.12f} BNB")
print(f"Target wallet: {TARGET_WALLET}")
print("="*70) 