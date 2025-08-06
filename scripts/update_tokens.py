# scripts/update_tokens.py

import hashlib
from datetime import datetime
import re
import os

# Step 1: Generate new tokens for the month
month_tag = datetime.utcnow().strftime("%b%Y").lower()  # e.g. sep2025
tokens = [f"ghost-{month_tag}-{i:02}" for i in range(1, 11)]
hashed_tokens = [hashlib.sha256(token.encode()).hexdigest() for token in tokens]

# Step 2: Format for JS array
hash_block = ",\n  ".join([f'"{h}"' for h in hashed_tokens])

# Step 3: Update index.html with new hash list
index_path = "index.html"
if os.path.exists(index_path):
    with open(index_path, "r", encoding="utf-8") as f:
        html = f.read()

    new_html = re.sub(
        r'const validHashes = \[\s*[^]]*?\]',
        f'const validHashes = [\n  {hash_block}\n]',
        html,
        flags=re.DOTALL
    )

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(new_html)

    print(f"✅ index.html updated with new token hashes for {month_tag}")
else:
    print("⚠️ index.html not found. Skipping file update.")

# Step 4: Append to token log file
log_path = "tokens/token_log.txt"
os.makedirs(os.path.dirname(log_path), exist_ok=True)

with open(log_path, "a", encoding="utf-8") as log_file:
    log_file.write(f"# === {month_tag.upper()} ===\n")
    for token, h in zip(tokens, hashed_tokens):
        log_file.write(f"{token}  -->  {h}\n")
    log_file.write("\n")

print(f"✅ Appended {len(tokens)} tokens to {log_path}")
