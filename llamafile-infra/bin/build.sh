#!/bin/bash

set -e

mkdir -p ../src/tmp/llamafile

llamafile="Meta-Llama-3.1-8B-Instruct.Q3_K_S.llamafile"
llamafileurl="https://huggingface.co/Mozilla/Meta-Llama-3.1-8B-Instruct-llamafile/resolve/main/$llamafile"

if [ ! -f "../src/tmp/llamafile/$llamafile" ]; then
    echo "Downloading $llamafile"
    curl -L "$llamafileurl" -o "../src/tmp/llamafile/$llamafile"
    if [[ $llamafile == *.llamafile ]]; then
        echo "Making $llamafile executable"
        chmod +x "../src/tmp/llamafile/$llamafile"
    fi
fi

cd ../
sam build