# searcher_agent.py
import os
from dotenv import load_dotenv

from langchain.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI

from researchlab.tools.searcher_tools import (
    SearchPapersTool,
    GetPaperMetadataTool,
    FindPDFLinkTool,
)
from langchain.agents import create_agent

load_dotenv()


class SearcherAgent:
    def __init__(self, openai_api_key: str = None, model: str = "gpt-4o-mini"):
        if openai_api_key:
            os.environ["OPENAI_API_KEY"] = openai_api_key

        # Create your tools
        self.tools = [
            SearchPapersTool(),
            GetPaperMetadataTool(),
            FindPDFLinkTool(),
        ]

        # Build LLM and bind tools (this *is* the agent now)
        self.llm = ChatOpenAI(model=model, temperature=0)

        self.prompt = SystemMessage(content = [
            {'type': "text",
            'text':"You are a research agent that MUST use tools to search scientific papers."},
        ])

        self.agent = create_agent(
            self.llm,
            tools=self.tools,
            system_prompt = self.prompt
        )

    def run_query(self, query: str):
        return self.agent.invoke({
            "messages": [HumanMessage(content=query)]
        })


if __name__ == "__main__":
    ag = SearcherAgent()
    result = ag.run_query("Find papers on LSTMs predicting solar activity.")
    print(result)
    metadata = result["response_metadata"]
    final_answer = ag.llm.invoke(f"Using the following tool outputs, generate a final, concise answer:\n\n{metadata}")
    print(final_answer.content)
