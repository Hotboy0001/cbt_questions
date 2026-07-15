import os
import glob
import re

for filepath in glob.glob("*.html"):
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    
    # Disable aggressive blur and visibilitychange listeners that conflict with the Failsafe Modal
    new_content = re.sub(
        r'addEventListener\(\s*[\'"](?:blur|visibilitychange)[\'"]', 
        'addEventListener("__DISABLED_ANTI_CHEAT__"', 
        content, 
        flags=re.IGNORECASE
    )
    
    if content != new_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Patched anti-cheat in {filepath}")

print("Done stripping blur and visibilitychange.")
