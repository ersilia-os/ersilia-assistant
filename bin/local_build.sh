# Script to locally set up Ersilia Assistant
#!/bin/bash

set -ex

# The directory where the script is run
# This is in the ersilia-assistant repository at ersilia-assistant/bin
WORKDIR=$(pwd)

# Directory for storing all the artifacts for this project
assistant_dir="$HOME/.ersilia-assistant"

# The llamafile to download
llamafile="Meta-Llama-3.1-8B-Instruct.Q3_K_S.llamafile"
llamafileurl="https://huggingface.co/Mozilla/Meta-Llama-3.1-8B-Instruct-llamafile/resolve/main/$llamafile"

llamafiledir="$assistant_dir/llamafile"
llamafile_path="$llamafiledir/$llamafile"

# Check Python version and if it is less than Python 3.10, raise an error and exit
if [[ $(python3 --version | cut -d " " -f 2 | cut -d "." -f 1) -lt 3 ]] || [[ $(python3 --version | cut -d " " -f 2 | cut -d "." -f 2) -lt 10 ]]; then
    echo "Python 3.10 or higher is required to run this script"
    exit 1
fi

# Check if the directory for storing the artifacts exists, if not, create it
if [ ! -d "$assistant_dir" ]; then
    mkdir -p "$assistant_dir"
fi

# Check if the directory for storing the llamafile exists, if not, create it
if [ ! -d "$llamafiledir" ]; then
    mkdir -p "$llamafiledir"
fi

# Download the llamafile if it does not exist
if [ ! -f "$llamafiledir/$llamafile" ]; then
    echo "Downloading $llamafile"
    curl -L "$llamafileurl" -o "$llamafile_path"
    if [[ $llamafile == *.llamafile ]]; then
        echo "Making $llamafile executable"
        chmod +x "$llamafiledir/$llamafile"
    fi
fi

# Check if the virtual environment exists, if not, create it
if [ ! -d "$assistant_dir/venv" ]; then
    python3 -m venv "$assistant_dir/venv"
fi

# Activate the virtual environment in a sub shell and install the dependencies
(
    source "$assistant_dir/venv/bin/activate"
    pip install --upgrade pip
    cd "$WORKDIR/.."
    pip install .
)

echo "Ersilia Assistant setup complete"
echo "Starting the assistant now!"

# Run the llamafile server at port 8080 in a sub shell
# The llamafile server is a simple HTTP server that serves the llamafile
(
    $llamafile_path \
    --server \
    --fast \
    --gpu DISABLE \
    --no-warmup \
    --timeout 600 \
    --nobrowser \
    --host 0.0.0.0 \
    --log-disable \
    --port 8080

    # Check if the llamafile server is already running
    if [ $? -eq 0 ]; then
        echo "Llamafile server is running at http://localhost:8080"
    else
        echo "Failed to start the llamafile server"
    fi
)

# Run the assistant in a sub shell
(
    source "$assistant_dir/venv/bin/activate"
    cd "$WORKDIR/.."
    streamlit run streamlit/app.py

    # Check if the assistant is already running
    if [ $? -eq 0 ]; then
        echo "Ersilia Assistant is running at http://localhost:8501"
    else
        echo "Failed to start the Ersilia Assistant"
    fi
)

echo "Ersilia Assistant is now available at http://localhost:8501"
echo "To report any issues, reach out to us at hello@ersilia.io"