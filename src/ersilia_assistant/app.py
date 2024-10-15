import streamlit as st

from summarizer_engine import Summarizer
from model_selector import ModelSelector
from recipe_generator import RecipeGenerator
from defaults import EOF_TOKEN

st.title("Ersilia Assistant")

# History storage for storing all user inputs
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []  # List of dict and not a dict of lists

summarizer = Summarizer()
model_selector = ModelSelector()
recipe_generator = RecipeGenerator()
# Display messages from history on app rerun
# This might be useful for troubleshooting
# However this won't persist if the app is restarted
# If we want that, we'll have to store this to a file or database
for message in st.session_state.messages:
    with st.chat_message(message["role"]):  # This is a chat message container
        st.markdown(message["content"])  # Why not use st.write() here?

if prompt := st.chat_input("What is up?"):  # This creates an input widget
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Store user message in chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant message in chat message container
    with st.chat_message("assistant"):
        summary_stream = summarizer.summarize(prompt)
        summary_response = st.write_stream(summary_stream)

        modelselection_stream = model_selector.select_models(prompt)
        modelselection_response = st.write_stream(modelselection_stream)

        recipe_stream = recipe_generator.generate(modelselection_response)
        recipe_response = st.write_stream(recipe_stream)
    # Add assistant message to chat history
    response = summary_response + modelselection_response + recipe_response
    st.session_state.messages.append({"role": "assistant", "content": response})
