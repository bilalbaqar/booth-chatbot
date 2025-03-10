from langchain_core.tools import tool
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from langchain_openai import OpenAI
from langchain.output_parsers import RegexParser
from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize file paths
current_file = Path(__file__)
BASE_DIR = current_file.parents[3]
docs_dir = BASE_DIR / "data" / "syllabus"
print(docs_dir)
# Create docs directory if it doesn't exist
docs_dir.mkdir(parents=True, exist_ok=True)

# Initialize the document loader and embeddings
def initialize_syllabus_loader():
    """Initialize the syllabus loader and embeddings."""
    try:
        # Check if docs directory is empty
        if not any(docs_dir.iterdir()):
            print(f"Warning: No PDF files found in {docs_dir}. Please add syllabus PDFs to this directory.")
            return None
            
        # Load PDF documents
        loader = DirectoryLoader(str(docs_dir), glob="./*.pdf", loader_cls=PyPDFLoader)
        documents = loader.load()
        
        if not documents:
            print(f"Warning: No PDF documents were loaded from {docs_dir}")
            return None
        
        # Split documents into chunks
        chunk_size_value = 1000
        chunk_overlap = 100
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size_value, 
            chunk_overlap=chunk_overlap,
            length_function=len
        )
        texts = text_splitter.split_documents(documents)
        
        # Create embeddings
        embeddings = FAISS.from_documents(texts, OpenAIEmbeddings())
        
        # Save and load embeddings (for persistence)
        embeddings.save_local("llm_faiss_index")
        embeddings = FAISS.load_local(
            "llm_faiss_index", 
            OpenAIEmbeddings(), 
            allow_dangerous_deserialization=True
        )
        
        return embeddings
    except Exception as e:
        print(f"Error initializing syllabus loader: {str(e)}")
        return None

# Initialize the QA chain
def initialize_qa_chain():
    """Initialize the question answering chain."""
    prompt_template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

    This should be in the following format:

    Question: [question here]
    Helpful Answer: [answer here]
    Score: [score between 0 and 100]

    Begin!

    Context:
    ---------
    {context}
    ---------
    Question: {question}
    Helpful Answer:"""
    
    output_parser = RegexParser(
        regex=r"(.*?)\nScore: (.*)",
        output_keys=["answer", "score"],
    )
    
    PROMPT = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"],
        output_parser=output_parser
    )
    
    return load_qa_chain(
        OpenAI(temperature=0), 
        chain_type="map_rerank", 
        return_intermediate_steps=True, 
        prompt=PROMPT
    )

# Initialize components at module level
embeddings = initialize_syllabus_loader()
chain = initialize_qa_chain()

@tool
def syllabus_qa(query: str):
    """
    A tool for answering questions about course syllabi at the Booth School of Business.
    
    This tool can:
    - Answer questions about course content, requirements, and policies
    - Provide information about course structure and organization
    - Explain grading policies and course expectations
    - Share details about course materials and resources
    
    Example questions:
    - "What are the prerequisites for Advanced Investments?"
    - "How is the final grade calculated in Financial Accounting?"
    - "What are the main topics covered in Operations Strategy?"
    
    Args:
        query (str): The question about the course syllabus
        
    Returns:
        dict: A dictionary containing the answer and reference text
    """
    try:
        if not embeddings or not chain:
            return "I apologize, but I cannot answer syllabus-related questions at the moment. The syllabus database has not been properly initialized. Please ensure that PDF syllabi are available in the docs directory."
            
        # Get relevant chunks
        relevant_chunks = embeddings.similarity_search_with_score(query, k=2)
        chunk_docs = [chunk[0] for chunk in relevant_chunks]
        
        # Get results from chain
        results = chain({"input_documents": chunk_docs, "question": query})
        
        # Create reference text
        text_reference = " ".join(doc.page_content for doc in results["input_documents"])
        
        return {
            "Answer": results["output_text"],
            "Reference": text_reference
        }
        
    except Exception as e:
        return f"Error processing syllabus query: {str(e)}"

# Example usage
if __name__ == "__main__":
    test_queries = [
        "What are the prerequisites for Entrepreneurial Selling?",
        "How is the final grade calculated in Negotiations?",
        "What are the main topics covered in Investments?"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        result = syllabus_qa(query)
        print(f"Response: {result}") 