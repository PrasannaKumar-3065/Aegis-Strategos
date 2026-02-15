import json

def format_aegis_prompt(entry):
    # 1. Extract Basic Info
    persona = entry['persona']
    input_data = entry.get('input_data', {})
    
    # 2. Extract specific fields (safe .get() returns None if missing)
    history = input_data.get('history')
    observations = input_data.get('observations')
    knowledge = input_data.get('knowledge_context')
    dom = input_data.get('dom_elements')
    image = input_data.get('image_context')
    
    # Tools are special: They go in System Prompt, not User Context
    tools_list = input_data.get('tools')
    tools_display = json.dumps(tools_list) if tools_list else "[None]"

    # 3. Build the Context Block DYNAMICALLY
    # We only add the string if the data is not None
    context_block = ""
    
    if history:
        context_block += f"[HISTORY]:\n{history}\n"
        
    if observations:
        # Handle cases where observation is a List or Dict vs String
        obs_str = json.dumps(observations) if isinstance(observations, (list, dict)) else str(observations)
        context_block += f"[OBSERVATIONS]:\n{obs_str}\n"
        
    if knowledge:
        context_block += f"[KNOWLEDGE]:\n{knowledge}\n"
        
    if dom:
        # DOM is usually a list of dicts, so we dump it to string
        dom_str = json.dumps(dom) if isinstance(dom, (list, dict)) else str(dom)
        context_block += f"[DOM]:\n{dom_str}\n"
        
    if image:
        # For text training, we just mention the image context exists
        context_block += f"[IMAGE_CONTEXT]:\n{image}\n"

    # 4. Construct the Template
    # Note: We keep the System Prompt clean. The "Tools" line changes based on input.
    text = f"""<|im_start|>system
You are Aegis. Current Mode: {persona}
Tools: {tools_display}<|im_end|>
<|im_start|>user
<CONTEXT_BLOCK>
{context_block}
</CONTEXT_BLOCK>

{entry['user_query']}<|im_end|>
<|im_start|>assistant
Thought: {entry['expected_output']['thought']}
Action: {entry['expected_output']['action']}
Final Answer: {entry['expected_output']['final_answer'] if entry['expected_output'].get('final_answer') else ''}<|im_end|>"""
    
    return text

# --- CONFIGURATION (Modify this for each phase) ---

input_file = "phase_7.jsonl"       # <-- CHANGE THIS FILE NAME for each phase
output_file = "aegis_phase7_train.jsonl"     # <-- CHANGE THIS FILE NAME for output

c = 0
# with open(input_file, 'r') as f, open(output_file, 'w') as out:
#     data = f.read().strip()
#     data = json.loads(data)
#     for content in data:
#         formatted_text = format_aegis_prompt(content)
#         json.dump({"text": formatted_text}, out, ensure_ascii=False)
#         out.write('\n')
#         c += 1
# print(f"Successfully processed {c} examples from {input_file}")
try:
    with open(input_file, 'r', encoding='utf-8') as f, open(output_file, 'w', encoding='utf-8') as out:
        for line in f:
            if not line.strip(): continue
            
            try:
                data = json.loads(line)
                formatted_text = format_aegis_prompt(data)
                
                # Unsloth/HuggingFace expects {"text": "..."}
                json.dump({"text": formatted_text}, out, ensure_ascii=False)
                out.write('\n')
                c += 1
            except json.JSONDecodeError:
                print("Skipping invalid JSON line")

    print(f"Successfully processed {c} examples from {input_file}")

except FileNotFoundError:
    print(f"Error: Could not find file {input_file}")