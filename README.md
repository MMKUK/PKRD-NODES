
# 🧠 PKRD-NODES

This repository handles decentralized PKRD node approvals using an AI-based trust engine.

---

## ✅ How to Apply as a PKRD Node

Anyone can request to become a PKRD node by following these steps:

### 1. Generate a Wallet

Use MetaMask or a tool like `eth_account` in Python:

```python
from eth_account import Account
acct = Account.create()
print("Wallet:", acct.address)
print("Private Key:", acct.key.hex())
```

---

### 2. Sign the Join Request Message

**Message to sign:**  
```
PKRD Node Join Request
```

Use your wallet or Python again:

```python
from eth_account import Account
from eth_account.messages import encode_defunct

acct = Account.from_key("YOUR_PRIVATE_KEY")
message = encode_defunct(text="PKRD Node Join Request")
signed = Account.sign_message(message, acct.key)
print("Signature:", signed.signature.hex())
```

---

### 3. Create a JSON file in this format:

Save it as:  
📁 `node_requests/your_wallet.json`

```json
{
  "wallet_address": "0xYourWalletAddress",
  "fingerprint": "cpu:i9|ram:64gb|os:linux",
  "signed_message": "0xYourSignatureHere",
  "timestamp": 1712345678
}
```

⏰ `timestamp` should be generated using:

```python
import time
int(time.time())
```

---

### 4. Submit Your File

- Add your `.json` file inside `node_requests/`
- Push a Pull Request to this repo
- Our **AI Verifier** will automatically approve or reject it

---

## 🤖 What Happens Next?

- Approved nodes are moved to the `/approved/` folder
- Rejected nodes may be logged in `/rejected/` (optional)
- PKRD AI runs all checks with zero human interaction

---

📢 Join the decentralized revolution. Let PKRD approve your node with pure code 🧠💚
