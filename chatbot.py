from llm_utils import get_context_from_prompt, ask_clarification
from scraper import fetch_products
from scorer import select_best_product

print("🤖 Hello! What are you looking for today?")
user_input = input("You: ")

# Step 1: Extract intent and entities using LLM
context = get_context_from_prompt(user_input)

# Step 2: Clarify missing details
required_slots = ['budget', 'brand', 'features']
for slot in required_slots:
    if slot not in context or not context[slot]:
        question = ask_clarification(slot)
        context[slot] = input(f"Chatbot: {question}\nYou: ")

print("\n🔍 Fetching matching products...")
products = fetch_products(context['product'], context['budget'])

# Step 3: Select best matching product
best_product = select_best_product(products, context)

print("\n✅ Best Product Match:")
print(f"Name: {best_product['name']}")
print(f"Price: ₹{best_product['price']}")
print(f"Rating: {best_product['rating']}")
print(f"Link: {best_product['link']}")