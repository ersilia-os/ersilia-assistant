# Ersilia Assistant

Find a live demo [here](https://ersilia-assistant.streamlit.app)!
A chat assistant to help users design experimental drug discovery workflows using Ersilia models with ease!

Below is a schema of how Ersilia Assistant development is guided

![Ersilia Assistant](assets/ersilia-assistant.jpeg)


## Development
This project requires Python version 3.10 or higher.

To get started, clone this repository and create a virtual environment, and install the dependencies

Note: Install the package in editable mode so you can easily review changes

```bash
source venv/bin/activate # Or your environment manager of choice

git clone https://github.com/ersilia-os/ersilia-assistant.git
cd ersilia-assistant
pip install -e .
```

Make sure you have installed a llamafile of your choice, for example, [Llama 3.1 8B-Instruct](https://huggingface.co/Mozilla/Meta-Llama-3.1-8B-Instruct-llamafile)

In a separate shell, run the following:

```bash

chmod +x /path/to/llamafile # You need to make the llamafile executable only once
./path/to/llamafile --server --nobrowser
```

Note: This is a blocking operation, and you should not close this shell. Optionally, you can use nohup to run this as a background process and exit the shell:

```bash
nohup ./path/to/llamafile --server --nobrowser &
```

You can verify that the llamafile server is running by opening a browser window and navigating to http://localhost:8080/

## Local Deployment

To deploy this entire setup locally, we have a simple script that creates necessary directories and installs the required assets as needed. To do this, run the following:

```bash
cd bin
./local-build
```

Since this project requires Python version 3.10 or higher, make sure that is the default Python version running in your shell.