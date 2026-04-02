import os

file_path = r'c:\Users\erick\.gemini\antigravity\scratch\FORXIME2\utils\assets_base64.py'

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")

# Clean the lines - remove trailing newlines and join them
cleaned_content = "".join([line.strip() for line in lines if line.strip()])

# We expect LOGO_B64 = '...data...'
# Let's ensure it's properly formatted. 
# If it's LOGO_B64 = '...data' on line 1 and ' on line 2, 
# stripe() will remove the newline and we'll get LOGO_B64 = '...data' or similar.

# Let's be more precise.
with open(file_path, 'r', encoding='utf-8') as f:
    full_text = f.read()

# Check for the broken quote
if "LOGO_B64 = '" in full_text:
    # Find the first quote
    first_quote_idx = full_text.find("'")
    # Find the last quote
    last_quote_idx = full_text.rfind("'")
    
    if first_quote_idx != -1 and last_quote_idx != -1 and first_quote_idx != last_quote_idx:
        # Extract the base64 part, removing any newlines or spaces inside
        header = full_text[:first_quote_idx+1]
        data = full_text[first_quote_idx+1:last_quote_idx].replace('\n', '').replace('\r', '').replace(' ', '')
        footer = full_text[last_quote_idx:]
        
        new_text = header + data + footer
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_text)
        print("File fixed successfully.")
    else:
        print("Could not find properly balanced quotes.")
else:
    print("Could not find LOGO_B64 assignment.")
