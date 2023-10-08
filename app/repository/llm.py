from getpass import getpass
import os
from langchain.llms import OpenAI, AzureOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import openai
from langchain.schema.vectorstore import VectorStoreRetriever
from app.database.config import OPENAI_API_KEY
from langchain.chains.question_answering import load_qa_chain


async def create_llm():
    # new_llm = OpenAI(openai_api_key=OPENAI_API_KEY)
    # template = """Question: {question}
    # Answer: """
    # prompt = PromptTemplate(template=template, input_variables=["question"])
    # llm_chain = LLMChain(memory = memory, prompt=prompt, llm=new_llm)
    new_llm = AzureOpenAI(temperature=0.5, max_tokens=500) 
    llm_chain = load_qa_chain(new_llm, chain_type="refine")
    return llm_chain


async def question_from_llm(llm: LLMChain, text:str):
    answer = llm.run(question=text)
    return answer