import json
import time
from eth_account import Account
from eth_account.messages import encode_defunct

# 🛠 Machine fingerprint info (adjust if needed)
fingerprint = "cpu:apple_m2|ram:32gb|os:macOS"

# 📩 Message to sign (must match verifier script)
message = "PKRD Node Join Request"
eth_message = encode_defunct(text=message)

# 🎲 Generate new Ethereum wallet
acct = Account.create()
wallet_address = acct.address
private_key = acct.key.hex()

# 🖋️ Sign the message
signed = Account.sign_message(eth_message, private_key)
signature = signed.signature.hex()

# 🕐 Current timestamp
timestamp = int(time.time())

# 🗂️ Prepare request JSON
node_data = {
    "wallet_address": wallet_address,
    "fingerprint": fingerprint,
    "signed_message": signature,
    "timestamp": timestamp
}

# 💾 Save JSON to file
filename = f"node_requests/{wallet_address.lower()}.json"
with open(filename, "w") as f:
    json.dump(node_data, f, indent=2)

# ✅ Display output
print("✅ Node request generated and saved:")
print("🔗 Wallet:", wallet_address)
print("🔐 Private Key:", private_key)
print("✍️ Signature:", signature)
print("🕐 Timestamp:", timestamp)
print("📄 File:", filename)
