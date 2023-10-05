from getpass import getpass
import os
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import openai

OPENAI_API_KEY = "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"
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY


async def create_llm(file_path: str):
    new_llm = OpenAI(openai_api_key=OPENAI_API_KEY)
    prompt = PromptTemplate(file_path)
    llm_chain = LLMChain(prompt=prompt, llm=new_llm)
    return llm_chain


async def question_from_llm(llm: LLMChain, text:str):
    return llm.run(text)