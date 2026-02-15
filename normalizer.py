import json
import os
import random

# --- CONFIGURATION ---
INPUT_FILE = "aegis_grand_model.jsonl" # The file you created in the last step
OUTPUT_FILE = "aegis_final_perfect.jsonl"

def normalize_row(data):
    """
    Ensures every row has the exact same schema:
    messages: [
      {
        "role": "system",
        "content": [ {"type": "text", "text": "..."} ] 
      },
      {
        "role": "user",
        "content": [ 
           {"type": "image", "image": "..." (optional)}, 
           {"type": "text", "text": "..."} 
        ]
      },
      {
        "role": "assistant",
        "content": [ {"type": "text", "text": "..."} ]
      }
    ]
    """
    messages = data.get("messages", [])
    new_messages = []
    
    for msg in messages:
        role = msg.get("role")
        content = msg.get("content")
        
        new_content = []
        
        # CASE 1: Content is already a list of dicts (The Vision Format)
        if isinstance(content, list) and len(content) > 0 and isinstance(content[0], dict):
            # It's already perfect, just keep it.
            # But ensure 'image' key is absent if not used, or handled correctly.
            new_content = content
            
        # CASE 2: Content is a String (The Text-Only Format)
        elif isinstance(content, str):
            new_content = [{"type": "text", "text": content}]
            
        # CASE 3: Content is a list of strings (Rare, but possible)
        elif isinstance(content, list) and len(content) > 0 and isinstance(content[0], str):
            new_content = [{"type": "text", "text": "".join(content)}]
            
        new_messages.append({
            "role": role,
            "content": new_content
        })
        
    return {"messages": new_messages}

def main():
    print(f"🚀 Normalizing {INPUT_FILE}...")
    valid_rows = []
    
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if not line.strip(): continue
            try:
                data = json.loads(line)
                normalized = normalize_row(data)
                valid_rows.append(normalized)
            except Exception as e:
                print(f"⚠️ Error line {i}: {e}")

    # Shuffle to mix text and vision thoroughly
    random.shuffle(valid_rows)

    print(f"💾 Saving {len(valid_rows)} normalized rows to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for row in valid_rows:
            f.write(json.dumps(row) + '\n')
            
    print("✅ Done! Use 'aegis_final_perfect.jsonl' in your training script.")

if __name__ == "__main__":
    main()