# import libraries
import os
from dotenv import load_dotenv

from langchain_openai import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate


# Make sure you have a variable called OPENAI_API_KEY in your .env file
load_dotenv(".env")


# create a prompt template
template = """Question: {question}

Answer: Let's think step by step.
"""
prompt = PromptTemplate(input_variables=['question'], template=template)


# load a model
llm = OpenAI(model="gpt-3.5-turbo-instruct", temperature=0.6, max_tokens=1028)


# create and run a chain
chain = prompt | llm
question = "Mary has 3 apples. She gives two to John and eats one." + \
" How many apples does she have left?"
out = chain.invoke({'question': question})
print(out)