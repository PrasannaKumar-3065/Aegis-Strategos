import json
INPUT_FILES=[
'aegis_phase2_train.jsonl',
'aegis_phase2_train.jsonl',
'aegis_phase3_train.jsonl',
'aegis_phase4_train.jsonl',
'aegis_phase5_train.jsonl',
'aegis_phase6_train.jsonl'
]

OUTPUT_FILE = 'aegis_dataset_merges_1_to_6.jsonl'
c = 0
json_data = []
for file in INPUT_FILES:
    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip(): continue
            
            try:
                data = json.loads(line) 
                json_data.append(data)               
                # Unsloth/HuggingFace expects {"text": "..."}
            except json.JSONDecodeError:
                print("Skipping invalid JSON line")

with open(OUTPUT_FILE, 'w', encoding='utf-8') as out:
    for json_d in json_data:
        json.dump(json_d, out, ensure_ascii=False)
        out.write('\n')
        c += 1

print(f"Successfully processed {c}")