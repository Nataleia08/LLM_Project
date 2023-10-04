from getpass import getpass
import os
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import openai


OPENAI_API_KEY = "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"
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
# os.environ["OPENAI_PROXY"] = "https://localhost:8000"


template = """Question: {question}

Answer: Let's think step by step."""

prompt = PromptTemplate(template=template, input_variables=["question"])

new_llm = OpenAI(openai_api_key=OPENAI_API_KEY)
llm_chain = LLMChain(prompt=prompt, llm=new_llm)

question = "What NFL team won the Super Bowl in the year Justin Beiber was born?"

print(llm_chain.run(question))