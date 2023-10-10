from getpass import getpass
import os
from langchain.llms import OpenAI, AzureOpenAI
from langchain.chains import LLMChain
from langchain.chains.question_answering import load_qa_chain


async def create_llm():
    new_llm = AzureOpenAI(temperature=0.5, max_tokens=500) 
    llm_chain = load_qa_chain(new_llm, chain_type="refine")
    return llm_chain


async def question_from_llm(llm: LLMChain, text:str):
    answer = llm.run(question=text)
    return answer