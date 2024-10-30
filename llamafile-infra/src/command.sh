#!/bin/sh
set -e

LLAMAFILE_PATH=${LLAMAFILE_PATH:-$(find "/opt/llamafile" -name "*.llamafile" -type f)}

echo "Starting llamafile ${LLAMAFILE_PATH}..."

# We might want to actually enable the GPU

$LLAMAFILE_PATH \
  --server \
  --fast \
  --threads "$(nproc)" \
  --gpu DISABLE \
  --no-warmup \
  --timeout 600 \
  --nobrowser \
  --host 0.0.0.0 \
  --log-disable \
  --port 8080
