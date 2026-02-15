import json
import re
import os

# --- CONFIGURATION ---
INPUT_FILES = [
    "phase_8.jsonl",   # Your Eyesight Dataset
    "phase_9.jsonl"   # Your Workflow/Tool Dataset
]
OUTPUT_FILE = "aegis_vision_master.jsonl"

def clamp(n):
    """Ensures coordinate is strictly between 0 and 1000."""
    try:
        n = int(n)
        return max(0, min(n, 1000))
    except ValueError:
        return 0

def fix_coordinates_in_text(text):
    """
    Scans text for [y1, x1, y2, x2] patterns and fixes values > 1000.
    """
    if not isinstance(text, str): return text
    
    # Regex for coordinates list: [100, 200, 300, 400]
    pattern = r"\[(\s*-?\d+\s*,\s*-?\d+\s*,\s*-?\d+\s*,\s*-?\d+\s*)\]"
    
    def replace_match(match):
        nums_str = match.group(1)
        parts = [p.strip() for p in nums_str.split(',')]
        clamped_parts = [str(clamp(p)) for p in parts]
        return f"[{', '.join(clamped_parts)}]"

    return re.sub(pattern, replace_match, text)

def merge_datasets():
    print(f"🚀 Starting Merge...")
    total_lines = 0
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as outfile:
        for fname in INPUT_FILES:
            if not os.path.exists(fname):
                print(f"⚠️ Warning: File {fname} not found. Skipping.")
                continue
                
            print(f"📂 Processing {fname}...")
            count = 0
            
            with open(fname, 'r', encoding='utf-8') as infile:
                for line in infile:
                    if not line.strip(): continue
                    
                    try:
                        data = json.loads(line)
                        
                        # 1. FIX COORDINATES IN THOUGHT (Crucial for Qwen2.5-VL)
                        if "expected_output" in data and "thought" in data["expected_output"]:
                            data["expected_output"]["thought"] = fix_coordinates_in_text(
                                data["expected_output"]["thought"]
                            )

                        # 2. STANDARDIZE IMAGE PATH
                        # Ensure 'image' field exists. If it's just a filename, you might want to keep it
                        # or prepend a path depending on your training loader. 
                        # For now, we assume the loader handles the path mapping.
                        
                        # 3. WRITE TO MASTER FILE
                        outfile.write(json.dumps(data) + '\n')
                        count += 1
                        total_lines += 1
                        
                    except json.JSONDecodeError:
                        print(f"❌ Error decoding line in {fname}")

            print(f"   -> Added {count} examples.")

    print(f"\n✅ SUCCESS: Merged dataset saved to {OUTPUT_FILE}")
    print(f"📊 Total Training Rows: {total_lines}")

if __name__ == "__main__":
    merge_datasets()