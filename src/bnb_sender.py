from web3 import Web3
import time

# Connect to BNB Smart Chain mainnet
print("Connecting to BNB Smart Chain...")
bsc = Web3(Web3.HTTPProvider('https://bsc-dataseed.binance.org/'))

# Check connection
if bsc.is_connected():
    print("Connected to BNB Smart Chain!")
else:
    print("Failed to connect to BNB Smart Chain!")
    exit(1)

# Target wallet address (where to consolidate all BNB)
TARGET_WALLET = "0xb72e9223dF0A6c247D6C2b955c3654eF28d0A32B"  # Replace with your target wallet

# Gas settings - based on current BSC network conditions
GAS_PRICE = bsc.to_wei('5', 'gwei')  # 5 Gwei
GAS_LIMIT = 21000  # Standard transfer gas limit
SAFETY_MARGIN = bsc.to_wei('0.00003', 'ether')  # Additional safety margin for transaction

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
        account = bsc.eth.account.from_key(private_key)
        from_address = account.address
        
        # Check account balance
        balance = bsc.eth.get_balance(from_address)
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
                'nonce': bsc.eth.get_transaction_count(from_address),
                'to': TARGET_WALLET,
                'value': amount_to_send,
                'gas': GAS_LIMIT,
                'gasPrice': GAS_PRICE,
                'chainId': 56  # BSC mainnet chain ID
            }
            
            # Sign transaction
            signed_tx = bsc.eth.account.sign_transaction(tx, private_key)
            
            # Send transaction
            try:
                # For newer web3.py versions
                tx_hash = bsc.eth.send_raw_transaction(signed_tx.raw_transaction)
            except AttributeError:
                # For older web3.py versions
                tx_hash = bsc.eth.send_raw_transaction(signed_tx.rawTransaction)
            
            tx_hash_hex = tx_hash.hex()
            amount_to_send_bnb = amount_to_send / (10**18)
            total_sent += amount_to_send_bnb
            
            print(f"Transaction successful: {amount_to_send_bnb:.12f} BNB")
            print(f"Transaction hash: {tx_hash_hex}")
            print(f"BSC Explorer: https://bscscan.com/tx/{tx_hash_hex}")
            print("-" * 70)
            
            success_count += 1
            
            # Add delay between transactions
            time.sleep(2)
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