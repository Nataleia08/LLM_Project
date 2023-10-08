from getpass import getpass
import os
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import openai
from langchain.schema.vectorstore import VectorStoreRetriever
from app.database.config import OPENAI_API_KEY


async def create_llm(memory:VectorStoreRetriever):
    new_llm = OpenAI(openai_api_key=OPENAI_API_KEY)
    # prompt = PromptTemplate(memory)
    llm_chain = LLMChain(memory = memory, llm=new_llm)
    return llm_chain


async def question_from_llm(llm: LLMChain, text:str):
    return llm.run(text)