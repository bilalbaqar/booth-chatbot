""" from langchain_core.tools import tool
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import CSVLoader
from langchain.vectorstores import DocArrayInMemorySearch
from IPython.display import display, Markdown
from langchain.llms import OpenAI
from langchain.embeddings.openai import OpenAIEmbeddings

from langchain.indexes import VectorstoreIndexCreator

from dotenv import load_dotenv
import os
# Load environment variables
load_dotenv()

file = os.path.abspath(r'..\data\all-course-list.csv')

loader = CSVLoader(file_path=file)

index = VectorstoreIndexCreator(
    vectorstore_cls=DocArrayInMemorySearch,
    embedding=OpenAIEmbeddings()
).from_loaders([loader])

query ="What is the course number for investments?"
query = "Give me 5 courses that are offered in Spring 2025?"

llm_replacement_model = OpenAI(temperature=0, 
                               model='gpt-3.5-turbo-instruct')









response = index.query(query, 
                       llm = llm_replacement_model)

display(Markdown(response))
print(response) """



from langchain_core.tools import tool
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import CSVLoader
from langchain.vectorstores import DocArrayInMemorySearch
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from dotenv import load_dotenv
from langchain.llms import OpenAI
import os

# Load environment variables
load_dotenv()

@tool
def csv_vector_search(question: str):
    """
    A tool for students at the Booth School of Business that provides insights into MBA course offerings, including schedules, faculty,
    locations, and enrollment capacities. 

    Capabilities:
    - Retrieve Course Schedules: Find when and where a course is being offered.
    - Identify Faculty Instructors: Get details about the professor teaching a course.
    - Fetch Course Numbers & Sections: Look up course numbers and section details.
    - Locate Classrooms: Identify the building and room for a given course.
    - Check Enrollment Capacity: View current and maximum student enrollment.
    - General Course Lookup: Answer questions such as:
        - "What courses are offered in Winter 2025?"
        - "Who is teaching Advanced Investments?"
        - "What time is 35150 scheduled?"
        - "Where is Financial Accounting being held?"
        - "What is the maximum capacity for Operations Strategy?"

    This tool is useful for anyone looking
    for quick insights into the course schedule database.
    """
    try:
        # Define the CSV file path
        file = os.path.abspath(r'..\data\all-course-list.csv')

        # Load the CSV data
        loader = CSVLoader(file_path=file)

        # Create a vector search index
        index = VectorstoreIndexCreator(
            vectorstore_cls=DocArrayInMemorySearch,
            embedding=OpenAIEmbeddings()
        ).from_loaders([loader])

        # Initialize LLM with retrieval model
        """ llm = ChatOpenAI(
            temperature=0,
            model='gpt-4o-mini'
        ) """
        # Initialize LLM with retrieval model
        llm = OpenAI(
            temperature=0, 
            model='gpt-3.5-turbo-instruct'
        )



        # Query the index
        response = index.query(question, llm=llm)
        return response

    except Exception as e:
        return f"Error processing query: {str(e)}"

# Example usage
if __name__ == "__main__":
    test_queries = [
        "What is the total number of records in the dataset?",
        "What are the column names in the dataset?",
        "What is the course number for investments?",
        "What are the course numbers for investments and financial accounting?",
        "What courses are offered in Spring 2025?",
        "What is the course number for Investments?",
        "Give me 5 courses that are offered in Spring 2025?",
        "Who is teaching Advanced Industrial Organization?",
        "Where is the Operations Strategy class being held?",
        "Which courses are available on Monday evenings?"
    ]

    for query in test_queries:
        print(f"\nQuery: {query}")
        print(f"Response: {csv_vector_search(query)}")