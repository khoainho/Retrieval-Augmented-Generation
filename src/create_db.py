import os
import shutil
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

DATA_SOURCE = "/Users/khoanguyen/Code/RAG/source_data/harry_potter_chapter_1.txt"
CHROMA_PATH = "chromaDB"
os.environ["OPENAI_API_KEY"] = "${PLACE YOUR API KEY HERE}"

def main():
    generate_data_store()

# Main function
def generate_data_store():
    docs = load_docs()
    chunks = split_text(docs)
    save_to_db(chunks)

# Load file into document 
# Document contain piece of text and associated metadata
def load_docs():
    loader = TextLoader(DATA_SOURCE)
    docs = loader.load()
    return docs

# Split the data in the documents into chucks for more consumable data
# Each chuncks are split into 700 characters because that is the average size of a paragraph in the document
def split_text(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        # Each chunk has 700 characters
        chunk_size=700,
        # Each chunk has an overlap of 50 characters
        chunk_overlap=50,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    return chunks

# Save chunks to Chroma DB with OpenAI
def save_to_db(chunks: list[Document]):
    # Clear all data from the database 
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    # Create a new Chroma DB from chunks and persist data 
    db = Chroma.from_documents(chunks, OpenAIEmbeddings(), persist_directory=CHROMA_PATH)
    db.persist()

if __name__ == "__main__":
    main()