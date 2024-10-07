import streamlit as st
from openai import OpenAI
from defaults import BASE_URL

st.title("Ersilia Assistant using LLama 3.1 run with Llamafile")
 
client = OpenAI(base_url=BASE_URL+"/v1", api_key="sk-no-key-required")

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "LlaMA_CPP"

# History storage for storing all user inputs
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [] # List of dict and not a dict of lists


# Display messages from history on app rerun
# This might be useful for troubleshooting
# However this won't persist if the app is restarted
# If we want that, we'll have to store this to a file or database
for message in st.session_state.messages:
    with st.chat_message(message["role"]): # This is a chat message container
        st.markdown(message["content"]) # Why not use st.write() here?

if prompt := st.chat_input("What is up?"): # This creates an input widget
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Store user message in chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant message in chat message container
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True
        )
        response = st.write_stream(stream) # This streaming thingy also shows a cursor which is kinda cool
    # Add assistant message to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

    

