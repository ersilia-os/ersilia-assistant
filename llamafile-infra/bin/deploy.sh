#!/bin/sh
set -e

./build.sh

if [ -f "../samconfig.toml" ]; then
  sam deploy --config-file samconfig.toml
else
  sam deploy --guided --stack-name "llamafile-lambda-python"
fi
