import os
import httpx
import streamlit as st


ASSISTANT_URL = os.environ.get("ASSISTANT_URL", "http://localhost:8000")

def run(query: str):
    query = query.strip() # Remove leading and trailing whitespaces
    url = f"{ASSISTANT_URL}/run?query={query}"
    with httpx.stream("GET", url, timeout=600.0) as r:
        for word in r.iter_text():
            yield word
        # for line in r.iter_lines():
        #     yield line

# Welcome page
st.title("Ersilia Assistant")

# Display a sidebar with information about the Ersilia Open Source Initiative
st.sidebar.title("About the Ersilia Open Source Initiative")

st.sidebar.warning(
    "This is an AI-based assistant and is intended for research use only. Please do not use this for clinical or commercial purposes."
)

# History storage for storing all user inputs
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []  # List of dict and not a dict of lists


# Initialize the assistant

# Display messages from history on app rerun
# This might be useful for troubleshooting
# However this won't persist if the app is restarted
# If we want that, we'll have to store this to a file or database
for message in st.session_state.messages:
    with st.chat_message(message["role"]):  # This is a chat message container
        st.markdown(message["content"])  # Why not use st.write() here?

if prompt := st.chat_input(
    "Ask me how to use the Ersilia Model Hub!"
):  # This creates an input widget
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Store user message in chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant message in chat message container
    with st.chat_message("assistant"):
        # Call the assistant API
        response = st.write_stream(run(prompt))

    # Add assistant message to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
