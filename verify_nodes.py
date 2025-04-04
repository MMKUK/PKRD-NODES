
import os
import json
import time
import shutil
import hashlib
from eth_account import Account
from eth_account.messages import encode_defunct

TRUST_THRESHOLD = 0.72
TIMESTAMP_WINDOW = 10

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
        print(f"[!] Signature validation failed for {wallet_address}: {e}")
        return False

def approve_node(wallet_address, fingerprint, signed_data, message, timestamp, node_file_path):
    now = int(time.time())
    delay = abs(now - timestamp)

    if delay > TIMESTAMP_WINDOW:
        print(f"❌ Skipping {wallet_address}: expired timestamp.")
        return

    if not validate_signature(wallet_address, signed_data, message):
        print(f"❌ Skipping {wallet_address}: invalid signature.")
        return

    entropy_score = get_entropy_score(fingerprint)
    trust_score = (entropy_score * 0.9) + 0.1
    print(f"🔍 {wallet_address} | Entropy: {entropy_score:.4f}, Trust: {trust_score:.4f}")

    if trust_score >= TRUST_THRESHOLD:
        approved_data = {
            "wallet_address": wallet_address,
            "entropy": entropy_score,
            "trust": trust_score,
            "approved_time": now
        }
        approved_file = f"approved/{wallet_address.lower()}.json"
        with open(approved_file, 'w') as f:
            json.dump(approved_data, f, indent=2)
        os.remove(node_file_path)
        print(f"✅ Node approved: {wallet_address}")
    else:
        print(f"❌ Node rejected (low trust): {wallet_address}")

def run_verifier():
    message = "PKRD Node Join Request"
    request_folder = "node_requests"
    for filename in os.listdir(request_folder):
        if filename.endswith(".json"):
            file_path = os.path.join(request_folder, filename)
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                approve_node(
                    wallet_address=data["wallet_address"],
                    fingerprint=data["fingerprint"],
                    signed_data=data["signed_message"],
                    message=message,
                    timestamp=int(data["timestamp"]),
                    node_file_path=file_path
                )
            except Exception as e:
                print(f"[!] Failed to process {filename}: {e}")

if __name__ == "__main__":
    run_verifier()
