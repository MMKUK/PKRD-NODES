# 🚀 PKRD Node (Permissionless)

This node can be run by **any user** without approval. Once started, it:

- Creates its wallet
- Automatically syncs and connects to the PKRD Genesis Chain
- Includes faucet + explorer + signer

### 🔧 Usage

```bash
chmod +x pkrd-node
./pkrd-node install     # First-time setup
./pkrd-node faucet      # Claim test PKRD
./pkrd-node explorer    # Show local block info
./pkrd-node auto-signer # Optional auto node validation simulation
