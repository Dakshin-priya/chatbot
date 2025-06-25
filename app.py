import streamlit as st
from llm_utils import get_context_from_prompt, ask_clarification
from scraper import fetch_products
from scorer import select_best_product

st.set_page_config(page_title="ChatGPT-like Product Recommender", layout="centered")
st.title("🛒 Chat with Your Product Assistant")

# Initialize session states
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "context" not in st.session_state:
    st.session_state.context = {}
if "current_slot" not in st.session_state:
    st.session_state.current_slot = None
if "awaiting_answer" not in st.session_state:
    st.session_state.awaiting_answer = False

# Chat interface
if not st.session_state.chat_history:
    with st.chat_message("assistant"):
        st.markdown("Hello! 👋 What are you looking for today?")

user_input = st.chat_input("Type your request...")

if user_input:
    st.session_state.chat_history.append(("user", user_input))
    st.chat_message("user").markdown(user_input)

    if not st.session_state.context:
        # First input: extract product context
        context = get_context_from_prompt(user_input)
        if isinstance(context, str):
            context = {"product": user_input}
        st.session_state.context.update(context)

    elif st.session_state.awaiting_answer and st.session_state.current_slot:
        # Capture answer to clarification question
        slot = st.session_state.current_slot
        st.session_state.context[slot] = user_input
        st.session_state.chat_history.append(("assistant", f"✅ Noted your {slot}: {user_input}"))
        st.session_state.awaiting_answer = False
        st.session_state.current_slot = None
        st.rerun()

    # Ask for one missing field at a time
    if not st.session_state.awaiting_answer:
        required_slots = ['budget', 'brand', 'features']
        for slot in required_slots:
            if not st.session_state.context.get(slot):
                st.session_state.current_slot = slot
                question = ask_clarification(slot)
                st.session_state.chat_history.append(("assistant", question))
                st.chat_message("assistant").markdown(question)
                st.session_state.awaiting_answer = True
                break

    # If all context is filled, move to product fetch
    if all(st.session_state.context.get(slot) for slot in ['budget', 'brand', 'features']) and not st.session_state.awaiting_answer:
        with st.spinner("🔍 Searching for products..."):
            products = fetch_products(
                st.session_state.context['product'],
                st.session_state.context['budget'],
                st.session_state.context['features'],
                st.session_state.context['brand']
            )
            if not products:
                response = "No products found. Try refining your request."
                st.chat_message("assistant").warning(response)
                st.session_state.chat_history.append(("assistant", response))
            else:
                best = select_best_product(products, st.session_state.context)
                match_score = best.get("match_percent", "N/A")
                response = f"✅ **Best Match:**\n\n🛍️ **{best['name']}**\n💰 **Price:** ₹{best['price']}\n⭐ **Rating:** {best['rating']}\n🎯 **Match:** {match_score}%\n🔗 [View Product]({best['link']})"
                st.chat_message("assistant").markdown(response)
                st.session_state.chat_history.append(("assistant", response))

# Display full chat history
for role, msg in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(msg)
