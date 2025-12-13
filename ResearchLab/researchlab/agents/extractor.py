import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage # As mensagens que o usuário envia e as mensagens do sistema (instruções para o modelo)
from langchain_core.output_parsers import StrOutputParser # Parser para garantir que a saída seja uma string
from langchain_openai.chat_models import ChatOpenAI # A classe que interage com o modelo de linguagem do Ollama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder # Para criar templates de prompts de chat
from langchain.agents import AgentExecutor, create_openai_tools_agent
from ..tools.searcher_tools import SearchPapersTool, GetPaperMetadataTool, FindPDFLinkTool
import requests

load_dotenv()

class ExtractorAgent():
    def __init__(self, openai_api_key: str= None, model: str = "gpt-5-nano"):
        self._openai_api_key = openai_api_key
        os.environ["OPENAI_API_KEY"] = openai_api_key

        self._llm = ChatOpenAI(
            model=model,
            streaming=True
        )
        # search_tool = SearchPapersTool()
        # metadata_tool = GetPaperMetadataTool()
        # pdf_tool = FindPDFLinkTool()

        # self._tools = [search_tool, metadata_tool, pdf_tool]

        self._prompt = ChatPromptTemplate.from_messages([
            ("system",
            """
            You are a research assistant agent specialized in downloading scientific papers and extract information from them.
                You MUST use the available tools when needed.
                
                Your workflow:
                1. Use download_papers to download relevant papers.
                2. For each paper, use extract_paper_info to extract relevant information from them.
                3. If the user needs the PDF, call find_pdf_link.
            """),
            MessagesPlaceholder("messages"),
            # Required by agent-style prompts to collect intermediate reasoning
            MessagesPlaceholder("agent_scratchpad")
        ])

        agent = create_openai_tools_agent(
            llm = self._llm,
            tools = self._tools,
            prompt = self._prompt
        )

        self.agent = AgentExecutor.from_agent_and_tools(
            agent=agent,
            tools=self._tools,
            verbose=True
        )




if __name__ == "__main__":
    searcher = SearcherAgent(openai_api_key=os.getenv("OPENAI_API_KEY"))
    response = searcher.agent.invoke({
    "messages": [
        {"role": "user", "content": "Find papers on using LSTMs to predict solar activity."}
    ]
})

print(response)

