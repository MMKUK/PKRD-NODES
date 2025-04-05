import hashlib

def zk_proof_generate(data):
    return {
        "proof": hashlib.sha256(data.encode()).hexdigest(),
        "data": data
    }

def zk_verify(proof_data):
    expected = hashlib.sha256(proof_data["data"].encode()).hexdigest()
    return expected == proof_data["proof"]
