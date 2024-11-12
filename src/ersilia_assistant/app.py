from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import uvicorn

from ersilia_assistant.agent import ErsiliaAssistant

app = FastAPI(debug=True)


def assistant_response(query: str):
    assistant = ErsiliaAssistant()
    # Since assistant.run is a blocking function, the generator is not async
    # Otherwise the response doesn't really 'stream', and ends up showing in a single block
    for token in assistant.run(query):
        yield token

@app.get("/")
def health():
    return {"status": "ok"}

@app.get("/run")
async def run(query: str):
    # Ref: https://stackoverflow.com/a/75760884
    return StreamingResponse(assistant_response(query), media_type="text/event-stream")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")