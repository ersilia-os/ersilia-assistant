import streamlit as st
import time
import os
from inputs import disease, dataset, objective, prompts, about
from PIL import Image

root = os.path.dirname(__file__)

# Function for the typing effect
def type_text(text, placeholder, delay=0.02):
    typed_text = ""
    for char in text:
        typed_text += char
        wrapped_text = f"""
        <div style="
            border: 1px solid #e6e6e6; 
            padding: 10px; 
            border-radius: 5px; 
            background-color: #d2d2d0; 
            color: #333; 
            font-family: sans-serif;  
            word-wrap: break-word;">
            {typed_text}
        </div>
        """
        placeholder.markdown(wrapped_text, unsafe_allow_html=True)
        time.sleep(delay)

@st.cache_data(show_spinner=False)
def load_images():
    images = {
        "M": Image.open(os.path.join(root,"images", "app-01.png")),
        "T": Image.open(os.path.join(root, "images", "app-03.png")),
        "C": Image.open(os.path.join(root, "images", "app-02.png")),
        "N": Image.open(os.path.join(root,"images", "app-05.png")),
        "S": Image.open(os.path.join(root,"images", "app-08.png")),
        "Select": Image.open(os.path.join(root,"images", "app-06.png")),
        "Toxic": Image.open(os.path.join(root,"images", "app-07.png")),
        "Expand": Image.open(os.path.join(root,"images", "app-04.png")),
    }
    return images

def clear_cache():
    keys = list(st.session_state.keys())
    for key in keys:
        st.session_state.pop(key)

images = load_images()

# Main application
st.set_page_config(layout="wide", page_title="Ersilia Self Service")

st.title("Ersilia Assistant")
st.write("Welcome to the Ersilia Assistant Demo, where you can put yourself in the shoes of a biomedical scientist! Select your preferred research program from the options below and see how can AI help you!")

# Initialize session state for selections
if "selections" not in st.session_state:
    st.session_state.selections = {"disease": None, "dataset": None, "objective": None}

# Step 1: Disease
st.subheader("Disease of interest:")
col1, col2, col3 = st.columns(3)

with col1:
    st.image(images["M"])
    for key, value in disease.items():
        if key == "M" and st.button(value, key=key, use_container_width=True):
            st.toast("Malaria selected")
            st.session_state.selections["disease"] = key

with col2:
    st.image(images["T"])
    for key, value in disease.items():
        if key == "T" and st.button(value, key=key, use_container_width=True):
            st.toast("Tuberculosis selected")
            st.session_state.selections["disease"] = key

with col3:
    st.image(images["C"])
    for key, value in disease.items():
        if key == "C" and st.button(value, key=key, use_container_width=True):
            st.toast("COVID-19 selected")
            st.session_state.selections["disease"] = key
    

# Step 2: Starting Library
st.subheader("Compound collection:")
col1, col2 = st.columns(2)

with col1:
    st.image(images["N"])
    for key, value in dataset.items():
        if key == "N" and st.button(value, key=key, use_container_width=True):
            st.toast("Natural products collection")
            st.session_state.selections["dataset"] = key

with col2:
    st.image(images["S"])
    for key, value in dataset.items():
        if key == "S" and st.button(value, key=key, use_container_width=True):
            st.toast("Synthetic compounds collection")
            st.session_state.selections["dataset"] = key

# Step 3: Objective
st.subheader("Research objective:")

col1, col2, col3 = st.columns(3)

with col1:
    st.image(images["Select"])
    for key, value in objective.items():
        if key == "Select" and st.button(value, key=key, use_container_width=True):
            st.toast("Best candidates query")
            st.session_state.selections["objective"] = key

with col2:
    st.image(images["Toxic"])
    for key, value in objective.items():
        if key == "Toxic" and st.button(value, key=key, use_container_width=True):
            st.toast("Toxicity query")
            st.session_state.selections["objective"] = key

with col3:
    st.image(images["Expand"])
    for key, value in objective.items():
        if key == "Expand" and st.button(value, key=key, use_container_width=True):
            st.toast("Library expansion query")
            st.session_state.selections["objective"] = key

# Display currently selected options
def selections_text(container):
    text = "### Current selections:\n"
    text += f"- **Disease:** {disease.get(st.session_state.selections['disease'], 'Not Selected')}\n"
    text += f"- **Dataset:** {dataset.get(st.session_state.selections['dataset'], 'Not Selected')}\n"
    text += f"- **Objective:** {objective.get(st.session_state.selections['objective'], 'Not Selected')}"
    container.write(text)

selections_text(st)

# Sidebar
st.sidebar.image(os.path.join(root, "images", "Ersilia_Brand_white_transp.png"))
st.sidebar.write("2024, Mozilla Builders Demo Day")
st.sidebar.write("\n-------\n")
selections_text(st.sidebar)
st.sidebar.write("\n-------\n")
st.sidebar.markdown("The [Ersilia Open Source Initiative](www.ersilia.io) is a tech **nonprofit organization** aimed at supporting **scientists in the Global South** with **AI/ML tools for drug discovery and infectious disease research**.")
for i in range(3):
    st.sidebar.write(about[i])

# Generate Query button
if None not in st.session_state.selections.values():
    if st.button(":thinking_face: Generate Query"):
        query_key = (
            st.session_state.selections["disease"],
            st.session_state.selections["dataset"],
            st.session_state.selections["objective"],
        )
        query = prompts.get(query_key, "No prompt available for the selected combination.")
        st.session_state.query = query  # Save the query in session state
        st.session_state['query_generated'] = True  # Mark query as generated
        placeholder = st.empty()  # Placeholder for typing effect
        type_text(query, placeholder)
    else:
        if "query_generated" in st.session_state:
            placeholder = st.empty()
            type_text(st.session_state.query, placeholder, delay=0)

else:
    st.info("Please complete all selections to generate a query.")

st.write("")
# Ask the Ersilia Assistant Button appears only after query is generated
if st.session_state.get('query_generated', False):
    if st.button(":robot_face: Ask the Ersilia Assistant"):
        # Load the response text from the JSON file
        file_name = "_".join(st.session_state.selections.values()) + ".txt"
        with open(os.path.join(root, "responses_edited", file_name), "r") as f:
            response_text = f.read()

        # Display the response with the typing effect
        response_placeholder = st.empty()  # Placeholder for typing effect
        type_text(response_text, response_placeholder)

# Reset app
        st.button(':recycle: Reset', on_click=clear_cache)