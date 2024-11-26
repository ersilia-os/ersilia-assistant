import streamlit as st
import time
import json
from inputs import disease, dataset, objective, prompts, about


# Function for the typing effect
def type_text(text, placeholder, delay=0.05):
    typed_text = ""
    for char in text:
        typed_text += char
        wrapped_text = f"""
        <div style="
            border: 1px solid #e6e6e6; 
            padding: 10px; 
            border-radius: 5px; 
            background-color: #f9f9f9; 
            color: #333; 
            font-family: monospace; 
            white-space: pre-wrap; 
            word-wrap: break-word;">
            {typed_text}
        </div>
        """
        placeholder.markdown(wrapped_text, unsafe_allow_html=True)
        time.sleep(delay)

# Main application
def main():
    st.title("Ersilia Assistant")
    st.write("Welcome to the Ersilia Assistant Demo, where you can put yourself in the shoes of a biomedical scientist! Select your preferred research program from the options below and see how AI can help you!")

    # Initialize session state for selections
    if "selections" not in st.session_state:
        st.session_state.selections = {"disease": None, "dataset": None, "objective": None}

    # Step 1: Disease
    st.subheader("Disease of interest:")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.image("images/malaria.jpg")
        for key, value in disease.items():
            if key == "M" and st.button(value, key=key, use_container_width=True):
                st.session_state.selections["disease"] = key

    with col2:
        st.image("images/tb.jpg")
        for key, value in disease.items():
            if key == "T" and st.button(value, key=key, use_container_width=True):
                st.session_state.selections["disease"] = key

    with col3:
        st.image("images/coronavirus.jpg")
        for key, value in disease.items():
            if key == "C" and st.button(value, key=key, use_container_width=True):
                st.session_state.selections["disease"] = key
        

    # Step 2: Starting Library
    st.subheader("Starting library:")
    col1, col2 = st.columns(2)

    with col1:
        st.image("images/plant.jpg")
        for key, value in dataset.items():
            if key == "N" and st.button(value, key=key, use_container_width=True):
                st.session_state.selections["dataset"] = key

    with col2:
        st.image("images/pills.jpg")  # Replace with actual image for Tuberculosis
        for key, value in dataset.items():
            if key == "S" and st.button(value, key=key, use_container_width=True):
                st.session_state.selections["dataset"] = key

    # Step 3: Objective
    st.subheader("Research objective:")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.image("images/petri_pipet.jpg")
        for key, value in objective.items():
            if key == "Select" and st.button(value, key=key, use_container_width=True):
                st.session_state.selections["objective"] = key

    with col2:
        st.image("images/flasks.jpg")  # Replace with actual image for Tuberculosis
        for key, value in objective.items():
            if key == "Toxic" and st.button(value, key=key, use_container_width=True):
                st.session_state.selections["objective"] = key

    with col3:
        st.image("images/multiwell.jpg")  # Replace with actual image for COVID-19
        for key, value in objective.items():
            if key == "Expand" and st.button(value, key=key, use_container_width=True):
                st.session_state.selections["objective"] = key

    # Display currently selected options
    st.write("### Current Selections:")
    st.write(f"**Disease:** {disease.get(st.session_state.selections['disease'], 'Not Selected')}")
    st.write(f"**Dataset:** {dataset.get(st.session_state.selections['dataset'], 'Not Selected')}")
    st.write(f"**Objective:** {objective.get(st.session_state.selections['objective'], 'Not Selected')}")

    # Generate Query button
    if None not in st.session_state.selections.values():
        if st.button("Generate Query"):
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

            # Show the "Ask the Ersilia Assistant" button after the query is typed
            st.markdown("<br>", unsafe_allow_html=True)  # Add some space between the query and the button
    else:
        st.info("Please complete all selections to generate a query.")

    # Ask the Ersilia Assistant Button appears only after query is generated
    if st.session_state.get('query_generated', False):
        if st.button("Ask the Ersilia Assistant"):
            # Load the response text from the JSON file
            with open("response.json", "r") as f:
                response_data = json.load(f)

            # Get the response text
            response_text = response_data.get("response", "No response found.")

            # Display the response with the typing effect
            response_placeholder = st.empty()  # Placeholder for typing effect
            type_text(response_text, response_placeholder)
if __name__ == "__main__":
    st.set_page_config(layout="wide", page_title="Ersilia Self Service")
    st.sidebar.image("images/Ersilia_Brand.png")
    st.sidebar.markdown("The [Ersilia Open Source Initiative](www.ersilia.io) is a tech **nonprofit organization** aimed at supporting research **scientists in the Global South** with **AI/ML tools for drug discovery and infectious disease research**.")
    for i in range(3):
        st.sidebar.write(about[i])
    

    main()
