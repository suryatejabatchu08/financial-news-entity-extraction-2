import spacy
import json
from spacy.training.example import Example
from spacy.scorer import Scorer

# 1. LOAD THE TRAINED MODEL
# Make sure this points to the folder where you saved the model
model_path = "financial_ner_model"
print(f"Loading model from: {model_path}...")
try:
    nlp = spacy.load(model_path)
except OSError:
    print(f"Error: Could not find model at '{model_path}'. Did you run the training script?")
    exit()

# 2. LOAD THE DEV DATA
# This is the 20% of data we held back specifically for this moment
data_path = "dev_financial_ner.json"
print(f"Loading validation data from: {data_path}...")
try:
    with open(data_path, "r") as f:
        dev_data = json.load(f)
except FileNotFoundError:
    print(f"Error: Could not find '{data_path}'. Did you run the dataset script?")
    exit()

# 3. PREPARE FOR EVALUATION
examples = []
print(f"Evaluating on {len(dev_data)} examples...")

for text, annotations in dev_data:
    # Create a Doc from the text (Prediction)
    doc_pred = nlp.make_doc(text)
    
    # Create an Example object which holds Prediction + Truth
    # This is required by SpaCy v3
    example = Example.from_dict(doc_pred, annotations)
    examples.append(example)

# 4. RUN EVALUATION
# nlp.evaluate() runs the model on all examples and calculates scores
scores = nlp.evaluate(examples)

# 5. DISPLAY RESULTS
print("\n" + "="*40)
print(f"{'METRIC':<15} | {'SCORE':<10}")
print("="*40)
print(f"{'Precision':<15} | {scores['ents_p']:.2%}")
print(f"{'Recall':<15} | {scores['ents_r']:.2%}")
print(f"{'F1-Score':<15} | {scores['ents_f']:.2%}")
print("="*40)

# 6. BREAKDOWN BY ENTITY TYPE
print("\nBreakdown by Entity Type:")
print(f"{'ENTITY':<12} | {'PRECISION':<10} | {'RECALL':<10} | {'F1':<10}")
print("-" * 48)

for entity_type, metrics in sorted(scores['ents_per_type'].items()):
    p = metrics['p']
    r = metrics['r']
    f = metrics['f']
    print(f"{entity_type:<12} | {p:.2%}    | {r:.2%}    | {f:.2%}")