#!/bin/bash
set -e

# Script to locally set up Ersilia Assistant
# The directory where the script is run
# This is in the ersilia-assistant repository at ersilia-assistant/bin
WORKDIR=$(pwd)

usage="$(basename "$0") [-h|--help|--start|--stop]
Locally setup Ersilia Assistant

where:
    -h, --help  Show this help text and exit
    --start     Start the Ersilia Assistant
    --stop      Stop the Ersilia Assistant"

if [[ $# -eq 0 ]] || [ "$1" == "-h" ] || [ "$1" == "--help" ]; then
    echo "$usage"
    exit 0
fi

while getopts ':hs:' option; do
    case "$option" in
        h) echo "$usage"
            exit 0
            ;;
    esac
done

if [ "$1" == "--start" ]; then
    echo "Starting the Ersilia Assistant"
elif [ "$1" == "--stop" ]; then
    echo "Stopping the Ersilia Assistant"
    pkill -f "streamlit run streamlit/app.py"
    pkill -f "$llamafile"
    exit 0
else
    echo "$usage"
    exit 1
fi

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

# Check if the nohup command is available, and if not, try to install it
if ! command -v nohup &> /dev/null; then
    echo "nohup command could not be found"
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "Trying to install nohup"
        sudo apt-get install nohup
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "Trying to install nohup"
        brew install nohup
    else
        echo "nohup command could not be installed"
        exit 1
    fi
fi

# Run the llamafile server at port 8080 in a sub shell
# The llamafile server is a simple HTTP server that serves the llamafile
(
    nohup $llamafile_path \
    --server \
    --fast \
    --gpu DISABLE \
    --no-warmup \
    --timeout 600 \
    --nobrowser \
    --host 0.0.0.0 \
    --log-disable \
    --port 8080 \
    &

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
    nohup streamlit run streamlit/app.py &

    # Check if the assistant is already running
    if [ $? -eq 0 ]; then
        echo "Ersilia Assistant is running at http://localhost:8501"
    else
        echo "Failed to start the Ersilia Assistant"
    fi
)

echo "Ersilia Assistant is now available at http://localhost:8501"
echo "To report any issues, reach out to us at hello@ersilia.io"