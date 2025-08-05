import hashlib
from datetime import datetime
import re

month_tag = datetime.utcnow().strftime("%b%Y").lower()
tokens = [f"ghost-{month_tag}-{i:02}" for i in range(1, 11)]
hashed_tokens = [hashlib.sha256(token.encode()).hexdigest() for token in tokens]

hash_block = ",\n  ".join([f'\"{h}\"' for h in hashed_tokens])

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

new_html = re.sub(
    r'const validHashes = \[\s*[^]]*?\]',
    f'const validHashes = [\n  {hash_block}\n]',
    html,
    flags=re.DOTALL
)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(new_html)

print(f"✅ Updated index.html with new token hashes for {month_tag}")
