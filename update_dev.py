import json
import re
import random

# --- BATCH 12: DEV SET UPDATE ---
# These are distinct from Training Batch 11 but test the same concepts.
batch_12_raw = [
    # TESTING INDICATORS (New Contexts)
    "The {Empire State manufacturing survey|INDICATOR} plummeted to -11.3 in January.",
    "Bond yields fell after the weak {ADP payrolls|INDICATOR} data was released.",
    "The {Core Personal Consumption Expenditures|INDICATOR} price index rose 0.3%.",
    "Investors ignored the better-than-expected {industrial production|INDICATOR} print.",
    "{Existing home sales|INDICATOR} dropped 1.9% as mortgage rates stayed high.",
    "The {Conference Board Consumer Confidence Index|INDICATOR} slid to 106.7.",
    "A surprise jump in {initial jobless claims|INDICATOR} suggests the labor market is softening.",
    
    # TESTING EVENTS (New Synonyms)
    "{Chevron|ORG} announced a $75 billion {share repurchase|EVENT} program.",
    "The {trading halt|EVENT} on {New York Community Bancorp|ORG} lasted for an hour.",
    "{Trian Partners|ORG} has built a significant {stake|EVENT} in {Allstate|ORG}.",
    "The market is entering a technical {correction|EVENT} after the 10% drop.",
    "{Reddit|ORG}'s {direct listing|EVENT} is expected to value the firm at $5 billion.",
    "A {short squeeze|EVENT} in {Root Inc.|ORG} sent the stock soaring 30%.",
    "{Japan|ORG} intervened to stop the {sell-off|EVENT} in the Yen.",
    "The {merger|EVENT} talks between {Warner Bros|ORG} and {Paramount|ORG} have stalled."
]

# --- CONVERSION LOGIC ---
def update_dev_file(new_lines, dev_file="dev_financial_ner.json"):
    # 1. Load Existing Dev Data
    try:
        with open(dev_file, "r") as f:
            existing_dev = json.load(f)
        print(f"Loaded {len(existing_dev)} existing Dev examples.")
    except FileNotFoundError:
        print(f"Error: Could not find {dev_file}. Make sure you generated the dataset first.")
        return

    # 2. Convert New Lines to Spacy Format
    new_data = []
    pattern = re.compile(r"\{(.*?)\|([A-Z]+)\}")
    
    for line in new_lines:
        clean_text = ""
        entities = []
        cursor = 0
        last_match_end = 0
        
        for match in pattern.finditer(line):
            pre_text = line[last_match_end:match.start()]
            clean_text += pre_text
            cursor += len(pre_text)
            
            entity_text = match.group(1)
            label = match.group(2)
            
            entities.append((cursor, cursor + len(entity_text), label))
            
            clean_text += entity_text
            cursor += len(entity_text)
            last_match_end = match.end()
            
        clean_text += line[last_match_end:]
        
        if entities:
            new_data.append((clean_text, {"entities": entities}))

    # 3. Merge (Append only)
    # We do NOT shuffle here because we want to ensure these specific tests are included
    updated_dev = existing_dev + new_data
    
    # 4. Save Back to File
    with open(dev_file, "w") as f:
        json.dump(updated_dev, f, indent=2)
        
    print(f"Success! Added {len(new_data)} new examples to the Dev Set.")
    print(f"New Dev Set Size: {len(updated_dev)}")

# --- EXECUTE ---
update_dev_file(batch_12_raw)