#!/bin/bash

set -e

mkdir -p ./tmp/llamafile

llamafile="Meta-Llama-3.1-8B-Instruct.Q5_K_S.llamafile"
llamafileurl="https://huggingface.co/Mozilla/Meta-Llama-3.1-8B-Instruct-llamafile/resolve/main/$llamafile"

if [ ! -f "./tmp/llamafile/$llamafile" ]; then
    echo "Downloading $llamafile"
    curl -L "$llamafileurl" -o "./tmp/llamafile/$llamafile"
    if [[ $llamafile == *.llamafile ]]; then
        echo "Making $llamafile executable"
        chmod +x "./tmp/llamafile/$llamafile"
    fi
fi

llamafileimage="ersiliaos/meta-llama-3-1-8b-instruct-q5-k-s-llamafile:latest"
cp ../dockerfiles/Dockerfile.llamafile ./

docker buildx build --platform linux/arm64 -t $llamafileimage -f Dockerfile.llamafile .

rm Dockerfile.llamafile