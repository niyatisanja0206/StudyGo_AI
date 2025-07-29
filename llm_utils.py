#llm_utils.py

import os
from dotenv import load_dotenv

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.chat_models import AzureChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun

# Load environment variables from .env file
load_dotenv()

def load_llm():
    """
    Loads Azure OpenAI GPT-4o LLM from environment configuration.
    """
    return AzureChatOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        model="gpt-4o",
        temperature=0.7,
        max_tokens=1500
    )

def create_chain(prompt_template: PromptTemplate):
    """
    Creates a LangChain LLMChain using GPT-4o and the provided prompt.
    """
    llm = load_llm()
    return LLMChain(llm=llm, prompt=prompt_template)

def get_duckduckgo_tool():
    """
    Returns the DuckDuckGo search tool instance from LangChain.
    """
    return DuckDuckGoSearchRun(name="DuckDuckGo Search")
