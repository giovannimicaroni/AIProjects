# ResearchLab

A FastAPI-based research assistant that helps you search and explore academic papers using the Semantic Scholar API. The application features an AI-powered agent that can intelligently search for papers, retrieve metadata, and find PDF links.

## Features

- **Intelligent Paper Search**: Natural language queries powered by LangChain agents
- **Comprehensive Metadata**: Access paper titles, authors, abstracts, citations, and more
- **PDF Discovery**: Automatically find direct PDF links for papers
- **Clean Web Interface**: Simple chat-based interface for interacting with the research agent
- **Secure API Key Management**: Session-based OpenAI API key storage

## Prerequisites

- Python 3.10 or higher
- OpenAI API key (for the LLM agent)

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd researchlab
```

2. Install dependencies using either pip or uv:

**Using pip:**
```bash
pip install -r requirements.txt
```

**Using uv (recommended):**
```bash
uv sync
```

3. Create a `.env` file in the project root (optional):
```bash
OPENAI_API_KEY=your-openai-api-key-here
```

## Project Structure

```
researchlab/
├── researchlab/
│   ├── agents/
│   │   └── searcher.py          # Main research agent implementation
│   ├── tools/
│   │   └── searcher_tools.py    # Semantic Scholar API tools
│   └── static/
│       ├── index.html           # Main chat interface
│       ├── settings.html        # API key configuration page
│       ├── chat.js              # Frontend JavaScript
│       └── style.css            # Styling
├── main.py                      # FastAPI application entry point
├── pyproject.toml              # Project dependencies
└── requirements.txt            # Alternative dependency list
```

## Usage

### Running the Application

1. Start the FastAPI server:
```bash
uvicorn main:app --reload
```

2. Open your browser and navigate to:
```
http://localhost:8000
```

3. On first visit, you'll be redirected to the settings page to enter your OpenAI API key

4. Start asking questions about research papers!

### Example Queries

- "Find papers on LSTMs predicting solar activity"
- "Search for recent work on transformer architectures"
- "What papers discuss quantum computing applications in cryptography?"
- "Find me papers by Geoffrey Hinton about deep learning"

### Using the Agent Programmatically

```python
from researchlab.agents.searcher import SearcherAgent

# Initialize the agent
agent = SearcherAgent(openai_api_key="your-key-here")

# Run a query
result = agent.run_query("Find papers on neural networks for climate modeling")
print(result)
```

## Available Tools

The research agent has access to three main tools:

1. **SearchPapersTool**: Search for papers using natural language queries
2. **GetPaperMetadataTool**: Retrieve detailed metadata for specific papers
3. **FindPDFLinkTool**: Locate direct PDF download links

## API Endpoints

- `GET /` - Main chat interface
- `GET /settings` - API key configuration page
- `POST /settings` - Save OpenAI API key to session
- `POST /chat` - Send a message to the research agent

## Rate Limiting

The application implements automatic retry logic with exponential backoff for the Semantic Scholar API to handle rate limiting (429 errors). If you encounter persistent rate limiting issues, consider:

- Adding a Semantic Scholar API key to the tools
- Reducing the frequency of requests
- Waiting between queries

## Configuration

### Changing the LLM Model

Edit `researchlab/agents/searcher.py`:

```python
self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
```

Available models include:
- `gpt-4o-mini` (default, cost-effective)
- `gpt-4o` (more capable)
- `gpt-3.5-turbo` (faster, cheaper)

### Session Secret Key

⚠️ **Important**: Change the session secret key in `main.py` before deploying:

```python
app.add_middleware(
    SessionMiddleware,
    secret_key="your-secure-random-key-here",  # Change this!
)
```

## Dependencies

Core dependencies:
- **FastAPI**: Web framework
- **LangChain**: Agent orchestration and tool management
- **OpenAI**: LLM provider
- **BeautifulSoup4**: HTML parsing for PDF link extraction
- **aiohttp**: Async HTTP requests
- **requests**: Synchronous HTTP requests

See `requirements.txt` or `pyproject.toml` for the complete list.

## Troubleshooting

### "API key not set" error
Make sure you've entered your OpenAI API key on the `/settings` page.

### Rate limiting errors
The Semantic Scholar API has rate limits. The application includes retry logic, but persistent errors may require waiting or adding an API key.

### Module import errors
Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

## Acknowledgments

- Powered by [Semantic Scholar API](https://www.semanticscholar.org/product/api)
- Built with [LangChain](https://www.langchain.com/)
- UI served by [FastAPI](https://fastapi.tiangolo.com/)

> The project in this repository was made by giovannimicaroni for learning purposes, and the owner is not responsible for it's further using.