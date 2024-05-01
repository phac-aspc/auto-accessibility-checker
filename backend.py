"""BACKEND.py

Helper functions for the frontend to load and run the model chain. 
Dependencies: `langchain_openai`, `langchain`, `openai`, `dotenv
"""

# import libraries
import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_text_splitters import Language, RecursiveCharacterTextSplitter


# Make sure you have a variable called OPENAI_API_KEY in your .env file
load_dotenv(".env")
KEY = os.getenv("OPENAI_API_KEY")

def get_chain(key : str = KEY, model : str = "gpt-3.5-turbo"):
    """ Initialises a model chain with the given API Key """

    # create a prompt template
    template = """You are a professional expert in accessible web design. You think methodically and say "I don't know" when you are uncertain.

    A client asks you for advice on how to make their website meet the W3C-WAI accessibility standards. Here is a snippet of their website's code:
    ```
        <p> Next, choose the years to show data for below: </p>
    </div>
    <div class="form-group">
        <h3 class="form-header" id="years-select-section">Years</h3>
        <div role="group">
            <ul class="checkboxes">
                <li><div role="checkbox" aria-checked="false">2018</div></li>
                <li><div role="checkbox" aria-checked="true">2019</div></li>
                <li><div role="checkbox" aria-checked="false">2020</div></li>
                <li><div role="checkbox" aria-checked="false">2021</div></li>
            </ul>
        </div>
    ```

    Your reasoning: Focusing only on W3C-WAI accessibility standards, I see the code snippet contains a group of checkboxes. However, the div with role group has no label. It requires an attribute like `aria-label` or `aria-labelledby` to provide a name for the group of checkboxes. Additionally, the checkboxes require a `tabindex="0"` attribute to ensure they can be focused on using the keyboard.
    Does the snippet meet W3C-WAI accessibility standards? (Yes/No): No. 

    A client asks you for advice on how to make their website meet the W3C-WAI accessibility standards. Here is a snippet of their website's code: 
    ```
    {code}
    ```

    Your reasoning: 
    """
    prompt = PromptTemplate(input_variables=['code'], template=template)


    # load a model
    llm = ChatOpenAI(model=model, temperature=0.7, max_tokens=512, 
                 api_key=key)
    chain = prompt | llm
    return chain

def chunkify(code : str) -> list:
    """ Splits the given file into smaller code snippets  """
    
    html_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.HTML, chunk_size=500, chunk_overlap=0
    )
    html_chunks = html_splitter.create_documents([code])

    return html_chunks

def analyse(chain, code : str) -> str:
    """ Analyses the given code snippet with the model chain """
    return chain.invoke({'code': code})