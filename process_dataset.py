
import json
import ast
import re
import os

# --- CONFIGURATION ---

# --- CONFIGURATION ---
INPUT_FILE = "aegis_vision_master.jsonl"  # The file you just pasted
OUTPUT_FILE = "aegis_phase7_ready.jsonl"

def clean_and_parse(line):
    line = line.strip()
    if not line: return None

    # 1. Fix Double Braces {{...}} -> {...}
    # This fixes the "unhashable type: 'dict'" error
    if line.startswith("{{") and line.endswith("}}"):
        line = line[1:-1]

    # 2. Try Standard JSON
    try:
        return json.loads(line)
    except json.JSONDecodeError:
        pass

    # 3. Try Python Eval (Handles single quotes)
    try:
        val = ast.literal_eval(line)
        if isinstance(val, dict):
            return val
    except (ValueError, SyntaxError, TypeError):
        pass

    # 4. Brute Force Regex (Fixing bad quotes)
    try:
        # Turn {'key': 'val'} into {"key": "val"}
        fixed = re.sub(r"(?<!\\)'(\w+)'\s*:", r'"\1":', line) # Keys
        fixed = re.sub(r":\s*'([^']*)'", r': "\1"', fixed)    # Simple values
        return json.loads(fixed)
    except:
        return None

def clamp_coordinates(text):
    """Safety: Ensures all coordinates in text are 0-1000."""
    if not isinstance(text, str): return text
    
    def replace_match(match):
        nums = [int(n.strip()) for n in match.group(1).split(',')]
        clamped = [str(max(0, min(n, 1000))) for n in nums]
        return f"[{', '.join(clamped)}]"

    return re.sub(r"\[(\s*-?\d+\s*,\s*-?\d+\s*,\s*-?\d+\s*,\s*-?\d+\s*)\]", replace_match, text)

def format_row(data):
    """Converts raw data to Unsloth Message Format"""
    
    # SYSTEM
    tools = data.get("available_tools") or data.get("input_data", {}).get("tools")
    tools_str = json.dumps(tools) if tools else "[None]"
    persona = data.get("persona", "ASSISTANT")
    system_content = f"You are Aegis. Current Mode: {persona}\nTools: {tools_str}"

    # USER (Image + Text)
    img_raw = data.get("image") or data.get("input_data", {}).get("image_context")
    if not img_raw: return None # Skip if no image
    
    input_d = data.get("input_data", {})
    context_str = "<CONTEXT_BLOCK>\n"
    if input_d.get("history"): context_str += f"[HISTORY]:\n{input_d['history']}\n"
    if input_d.get("dom_elements"): context_str += f"[DOM]:\n{json.dumps(input_d['dom_elements'])}\n"
    if input_d.get("observations"): context_str += f"[OBSERVATIONS]:\n{input_d['observations']}\n"
    if input_d.get("knowledge_context"): context_str += f"[KNOWLEDGE]:\n{input_d['knowledge_context']}\n"
    context_str += "</CONTEXT_BLOCK>\n\n"
    
    user_text = f"{context_str}{data.get('user_query', '')}"

    # ASSISTANT
    out = data.get("expected_output", {})
    thought = clamp_coordinates(out.get("thought", ""))
    action = out.get("action", "None")
    if isinstance(action, dict): action = json.dumps(action)
    
    final_resp = f"Thought: {thought}\nAction: {action}"
    if out.get("final_answer"): final_resp += f"\nFinal Answer: {out['final_answer']}"
    if out.get("goal") == "achieved": final_resp += "\n[GOAL ACHIEVED]"

    return {
        "messages": [
            {"role": "system", "content": system_content},
            {
                "role": "user", 
                "content": [
                    {"type": "image", "image": str(img_raw)},
                    {"type": "text", "text": user_text}
                ]
            },
            {"role": "assistant", "content": [{"type": "text", "text": final_resp}]}
        ]
    }

def main():
    print(f"🧹 Cleaning and Converting {INPUT_FILE}...")
    success = 0
    failed = 0
    
    # Create input file from your paste if needed, or rely on existing file
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Error: {INPUT_FILE} not found. Please save your raw data with this name.")
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f_in, \
         open(OUTPUT_FILE, 'w', encoding='utf-8') as f_out:
        
        for line in f_in:
            data = clean_and_parse(line)
            if data:
                formatted = format_row(data)
                if formatted:
                    f_out.write(json.dumps(formatted) + '\n')
                    success += 1
                else:
                    failed += 1
            else:
                failed += 1

    print(f"✅ Finished!")
    print(f"   Success: {success}")
    print(f"   Failed: {failed}")
    print(f"   Output: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()