from chain import chain
from fastapi import FastAPI
from langserve import add_routes

app = FastAPI(title="AI Translator", description="An AI-powered translator using Mistral model via Ollama", version="1.0.0")

add_routes(app, chain, path="/translate")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)