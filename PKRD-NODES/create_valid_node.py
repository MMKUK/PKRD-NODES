import json
import time
from eth_account import Account
from eth_account.messages import encode_defunct

# ✅ Create Wallet
acct = Account.create()
wallet = acct.address
private_key = acct.key.hex()

# ✅ Message
msg = "PKRD Node Join Request"
eth_msg = encode_defunct(text=msg)

# ✅ Sign it NOW with fresh timestamp
signature = "0x" + Account.sign_message(eth_msg, private_key).signature.hex()

# ✅ Create correct data
node_data = {
    "wallet_address": wallet,
    "fingerprint": "cpu:apple_m2|ram:32gb|os:macOS",
    "signed_message": signature,
    "timestamp": int(time.time())
}

# ✅ Save into node_requests/
filename = f"node_requests/{wallet.lower()}.json"
with open(filename, "w") as f:
    json.dump(node_data, f, indent=2)

print("✅ Wallet:", wallet)
print("🔐 Private Key:", private_key)
print("✍️ Signature:", signature)
print("📄 Saved:", filename)
