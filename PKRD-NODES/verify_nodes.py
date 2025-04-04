import os
import json
import time
import hashlib
from eth_utils import decode_hex
from eth_account import Account
from eth_account.messages import encode_defunct

# Trust & Time thresholds
TRUST_THRESHOLD = 0.4
TIMESTAMP_WINDOW = 10  # seconds

# Folders
requests_folder = "node_requests"
approved_folder = "approved"
rejected_folder = "rejected"

os.makedirs(approved_folder, exist_ok=True)
os.makedirs(rejected_folder, exist_ok=True)

approved_nodes = {}
penalized_nodes = {}

# Entropy score
def get_entropy_score(fingerprint: str) -> float:
    hash_val = hashlib.sha256(fingerprint.encode()).hexdigest()
    entropy = sum([int(c, 16) for c in hash_val[:10]]) / 160.0
    return min(1.0, entropy)

# Signature verification
def validate_signature(wallet_address: str, signed_data: str, message: str) -> bool:
    try:
        eth_message = encode_defunct(text=message)
        
        # Remove "0x" from signature if present
        sig_bytes = decode_hex(signed_data[2:] if signed_data.startswith("0x") else signed_data)
        
        # Recover address
        recovered = Account.recover_message(eth_message, signature=sig_bytes)
        return recovered.lower() == wallet_address.lower()

    except Exception as e:
        print(f"[!] Signature validation failed: {e}")
        return False

# Node decision logic
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

    print(f"🧠 Entropy Score: {entropy_score:.4f}, Trust Score: {trust_score:.4f}")

    if trust_score >= TRUST_THRESHOLD:
        approved_nodes[wallet_address] = {
            "approved_time": now,
            "entropy": entropy_score,
            "trust": trust_score
        }
        return True

    return False

# Run approvals
for filename in os.listdir(requests_folder):
    if filename.endswith(".json"):
        with open(os.path.join(requests_folder, filename)) as f:
            data = json.load(f)

        wallet = data["wallet_address"]
        print(f"🧪 Processing request: {wallet}")

        approved = should_approve_node(
            wallet_address=data["wallet_address"],
            fingerprint=data["fingerprint"],
            signed_data=data["signed_message"],
            message="PKRD Node Join Request",
            request_timestamp=data["timestamp"]
        )

        if approved:
            os.rename(
                os.path.join(requests_folder, filename),
                os.path.join(approved_folder, filename)
            )
            print(f"✅ Approved: {wallet}")
        else:
            os.rename(
                os.path.join(requests_folder, filename),
                os.path.join(rejected_folder, filename)
            )
            print(f"❌ Rejected: {wallet}")
