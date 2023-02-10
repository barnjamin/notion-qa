"""Ask a question to the notion database."""
import faiss
import pickle
import argparse

from langchain import OpenAI
from langchain.chains import VectorDBQAWithSourcesChain

from prompts import question_prompt, combine_prompt, example_prompt

parser = argparse.ArgumentParser(description="Ask a question to the docs DB.")
parser.add_argument("question", type=str, help="The question to ask the docs DB")
args = parser.parse_args()

# Load the LangChain.
with open("faiss_store.pkl", "rb") as f:
    store = pickle.load(f)
store.index = faiss.read_index("docs.index")
text="text-curie-001"
code="code-cushman-001"	
chain = VectorDBQAWithSourcesChain.from_llm(
    llm=OpenAI(temperature=0, model_name=code),
    vectorstore=store,
    question_prompt=question_prompt,
    combine_prompt=combine_prompt,
    document_prompt=example_prompt,
)

result = chain({"question": args.question})
print(f"Answer: {result['answer']}")
print(f"Sources: {result['sources']}")
