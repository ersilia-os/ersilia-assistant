FROM python:3.10-bullseye

# This is very stupid, I hate it, but I cannot get dockerignore to work
#TODO: Fix this
WORKDIR /app
COPY ./src ./src
COPY ./pyproject.toml .
# Otherwise pip complains about missing README.md and LICENSE
COPY ./README.md . 
COPY ./LICENSE .

RUN pip install --no-cache-dir . && \
    rm -rf /root/.cache/pip && \
    rm -rf /var/lib/apt/lists/*

ENV LLAMA_SERVER="http://localhost:8080"
ENTRYPOINT ["python", "src/ersilia_assistant/app.py"]