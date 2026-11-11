import getpass
from web3 import Web3

print("\n[NEXUS] Bridging APERTURE-7 to Live Network...")

# Connecting to the RPC endpoint you pinged earlier
rpc_url = "https://rpc-amoy.polygon.technology/"
web3 = Web3(Web3.HTTPProvider(rpc_url))

if not web3.is_connected():
    print("[!] Network connection failed.")
    exit()

print("[+] Connected to Polygon Amoy. Socket open.")

# Secure runtime injection (input will be invisible as you type)
private_key = getpass.getpass("         [SECURITY] Inject Private Key:0x1307fb41da02174e0efc3b6a10cb20da08b11fad7fa5d275e85415b9fa8d4633 ")

try:
    account = web3.eth.account.from_key(private_key)
    print(f"         [+] Wallet authenticated: {account.address}")
except Exception:
    print("         [!] Invalid key matrix.")
    exit()

print("[APERTURE-7] Applying flattened gas vectors (Gas = 0.0000)...")
nonce = web3.eth.get_transaction_count(account.address)

# Constructing a 0-value self-transfer to test the execution
tx = {
    'nonce': nonce,
    'to': account.address,
    'value': 0,
    'gas': 21000,
    'gasPrice': 0, 
    'chainId': 80002
}

print("[NEXUS] Signing cryptographic payload...")
signed_tx = web3.eth.account.sign_transaction(tx, private_key)

print("-" * 55)
print("[SYSTEM] Broadcasting real payload to Polygon mempool...")

try:
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print(f"[SUCCESS] Trade Secured. Live Network Hash: {web3.to_hex(tx_hash)}")
except Exception as e:
    print(f"\n[ANOMALY] Network Node Rejection: {e}")
    print("[!] The live consensus protocol refused the 0-gas spatial override.")

print("-" * 55)
print("[SYSTEM] One-shot complete. Shutting down for the night.")
