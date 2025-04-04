import time
import hashlib
import json
import os
from eth_account import Account
from eth_account.messages import encode_defunct

TRUST_THRESHOLD = 0.72
TIMESTAMP_WINDOW = 10  # seconds

approved_folder = "approved"
requests_folder = "node_requests"

approved_nodes = {}
penalized_nodes = {}

def get_entropy_score(fingerprint: str) -> float:
    hash_val = hashlib.sha256(fingerprint.encode()).hexdigest()
    entropy = sum([int(c, 16) for c in hash_val[:10]]) / 160.0
    return min(1.0, entropy)

def validate_signature(wallet_address: str, signed_data: str, message: str) -> bool:
    try:
        eth_message = encode_defunct(text=message)
        recovered_address = Account.recover_message(eth_message, signature=signed_data)
        return recovered_address.lower() == wallet_address.lower()
    except Exception as e:
        print(f"[!] Signature validation failed: {e}")
        return False

def should_approve_node(wallet_address, fingerprint, signed_data, message, request_timestamp):
    now = int(time.time())
    delay = abs(now - request_timestamp)

    if wallet_address in penalized_nodes:
        return False
    if wallet_address in approved_nodes:
        return False
    if delay > TIMESTAMP_WINDOW:
        return False
    if not validate_signature(wallet_address, signed_data, message):
        return False

    entropy_score = get_entropy_score(fingerprint)
    trust_score = (entropy_score * 0.9) + 0.1

    if trust_score >= TRUST_THRESHOLD:
        approved_nodes[wallet_address] = {
            "approved_time": now,
            "entropy": entropy_score,
            "trust": trust_score
        }
        return True
    return False

# 🚀 Begin processing all requests
for filename in os.listdir(requests_folder):
    path = os.path.join(requests_folder, filename)
    with open(path, "r") as f:
        data = json.load(f)
        wallet = data["wallet_address"]
        fingerprint = data["fingerprint"]
        signature = data["signed_message"]
        timestamp = data["timestamp"]
        message = "PKRD Node Join Request"

        print(f"🧪 Processing request: {wallet}")
        approved = should_approve_node(wallet, fingerprint, signature, message, timestamp)

        if approved:
            print("✅ Approved:", wallet)
            with open(os.path.join(approved_folder, filename), "w") as out:
                json.dump(data, out, indent=2)
        else:
            print("❌ Rejected:", wallet)
