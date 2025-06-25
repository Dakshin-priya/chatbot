from models.flan_t5 import flan_t5_infer
import json

import re
from models.flan_t5 import flan_t5_infer
import json

def get_context_from_prompt(prompt):
    try:
        extract_prompt = f"""
Extract from the user's message:
"{prompt}"
Return JSON with keys: product, budget, brand, features. Use 'null' for unknowns.
"""
        result = flan_t5_infer(extract_prompt)
        if isinstance(result, str):
            result = json.loads(result)
    except:
        result = {}

    # Fallback pattern extraction
    if 'budget' not in result or not result['budget']:
        match = re.search(r"(?:under|below|less than) ?₹?([0-9]+)", prompt, re.IGNORECASE)
        if match:
            result['budget'] = match.group(1)

    if 'features' not in result or not result['features']:
        color_match = re.search(r"(black|white|red|blue|green|grey|brown)", prompt, re.IGNORECASE)
        if color_match:
            result['features'] = color_match.group(1) + " color"

    if 'product' not in result or not result['product']:
        result['product'] = prompt.strip()

    return result


def ask_clarification(slot):
    fixed_questions = {
        "budget": "💰 What is your approximate budget?",
        "brand": "🏷️ Do you have any brand preference?",
        "features": "🛠️ Are there any specific features you're looking for?"
    }
    return fixed_questions.get(slot, f"Please provide your {slot}.")
