import os
import argparse
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma
from langchain.prompts import ChatPromptTemplate

CHROMA_PATH = "chromaDB"
os.environ["OPENAI_API_KEY"] = "${PLACE YOUR API KEY HERE}"

# Repsonse prompt template
PROMPT_TEMPLATE = """
Answer:

{context}

---------------------------------------

Answer based on the question: {question}
"""


def main():
    # Create CLI for user imput
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text

    # Connection to Chroma DB
    embedding_function = OpenAIEmbeddings()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search Chroma DB for relavant info based on user's prompt
    results = db.similarity_search_with_relevance_scores(query_text, k=3)
    if len(results) == 0 or results[0][1] < 0.7:
        print(f"Unable to find matching results.")
        return

    context_text = "\n\n---------------------------------------\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    print(prompt)

    model = ChatOpenAI()
    response_text = model.invoke(prompt)

    sources = [doc.metadata.get("source", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)


if __name__ == "__main__":
    main()