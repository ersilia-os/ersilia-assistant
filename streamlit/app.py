import streamlit as st

from ersilia_assistant import ErsiliaAssistant

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
assistant = ErsiliaAssistant()

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
        bot_stream = assistant.run(prompt)
        response = st.write_stream(bot_stream)

    # Add assistant message to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
