import json
import re
import random

# --- BATCH 11: THE REPAIR BATCH ---
# Focused purely on synonyms for EVENT and contexts for INDICATOR
batch_11_raw = [
    # INDICATOR REPAIRS (Contextual clues like 'reading', 'print', 'data')
    "The latest {JOLTS job openings|INDICATOR} data signaled a cooling labor market.",
    "Traders reacted negatively to the hot {Core CPI|INDICATOR} print this morning.",
    "The {Empire State Manufacturing Index|INDICATOR} plummeted to -14.5.",
    "Watch the {ADP Employment Change|INDICATOR} figures closely before the official jobs report.",
    "{U.S. crude oil inventories|INDICATOR} rose by 3 million barrels, pressuring prices.",
    "The {Case-Shiller Home Price Index|INDICATOR} showed a 5% year-over-year increase.",
    "Investors are waiting for the {flash PMI|INDICATOR} readings from Europe.",
    "{German ZEW Economic Sentiment|INDICATOR} improved slightly in November.",
    "The {Philly Fed Index|INDICATOR} came in below expectations.",
    "{China's Caixin Services PMI|INDICATOR} remained in expansion territory.",
    "A surprise drop in {Retail Sales|INDICATOR} sparked recession fears.",
    "The {University of Michigan Consumer Sentiment|INDICATOR} reading hit a six-month high.",
    "{Weekly jobless claims|INDICATOR} fell to 210,000, showing resilience.",
    "The {PCE Deflator|INDICATOR} is the Fed's favorite inflation gauge.",
    "{Durable Goods Orders|INDICATOR} rebounded thanks to aircraft demand.",

    # EVENT REPAIRS (Synonyms: Buyout, Stake, Halt, Sell-off, Correction)
    "{Berkshire Hathaway|ORG} acquired a massive {stake|EVENT} in {Chubb|ORG}.",
    "Trading was paused due to a {volatility halt|EVENT} after the stock dropped 20%.",
    "The market entered a {correction|EVENT} after falling 10% from highs.",
    "A massive {sell-off|EVENT} in tech stocks dragged the Nasdaq down.",
    "{Elliott Management|ORG} launched a {tender offer|EVENT} for {Crown Castle|ORG}.",
    "The {private placement|EVENT} raised $50 million for the biotech startup.",
    "{GameStop|ORG} announced a {stock split|EVENT} to make shares more affordable.",
    "The sudden {rally|EVENT} in bond yields spooked equity investors.",
    "{Saudi Arabia|ORG} announced a voluntary {production cut|EVENT} of 1 million barrels.",
    "The {liquidity injection|EVENT} by the central bank calmed the banking crisis.",
    "{Disney|ORG} faced a {proxy battle|EVENT} from activist investors.",
    "The {rebalancing|EVENT} of the Nasdaq 100 index forced funds to sell big tech.",
    "{SoftBank|ORG} is considering a {block sale|EVENT} of its Alibaba shares.",
    "The {de-listing|EVENT} of {Didi|ORG} from the NYSE was completed today.",
    "A {short squeeze|EVENT} sent shares of {Carvana|ORG} up 40% in one day."
]

# --- CONVERSION FUNCTION ---
def convert_and_merge(new_lines, existing_file="train_financial_ner.json"):
    # 1. Load Existing Data
    try:
        with open(existing_file, "r") as f:
            existing_data = json.load(f)
        print(f"Loaded {len(existing_data)} existing examples.")
    except FileNotFoundError:
        print(f"Error: Could not find {existing_file}. Run the previous generator script first.")
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

    # 3. Merge and Shuffle
    combined_data = existing_data + new_data
    random.shuffle(combined_data)
    
    # 4. Save Back to File
    with open(existing_file, "w") as f:
        json.dump(combined_data, f, indent=2)
        
    print(f"Success! Added {len(new_data)} new repair examples.")
    print(f"Total Training Dataset Size: {len(combined_data)}")

# --- RUN IT ---
convert_and_merge(batch_11_raw)