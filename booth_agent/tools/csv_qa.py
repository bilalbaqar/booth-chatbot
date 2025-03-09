from langchain_openai import ChatOpenAI
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

class CSVQuestionAnswerer:
    def __init__(self, csv_file_path: str):
        """
        Initialize the CSV Question Answerer.
        
        Args:
            csv_file_path (str): Path to the CSV file to load
        """
        # Initialize the language model
        self.llm = ChatOpenAI(
            temperature=0,
            model="gpt-4o-mini"
        )
        
        # Load the CSV file
        self.loader = CSVLoader(
            file_path=csv_file_path,
            encoding="utf-8",
            csv_args={
                'delimiter': ',',
                'quotechar': '"'
            }
        )
        
        # Load the documents
        self.documents = self.loader.load()
        
        # Create a context string from the CSV data
        self.context = self._create_context()
        
        # Create the prompt template
        self.prompt = PromptTemplate(
            template="""You are an assistant that helps answer questions about data from a CSV file.
            
            Here is the data from the CSV file:
            {context}
            
            Please answer the following question about this data:
            Question: {question}
            
            Provide a clear and concise answer based only on the information available in the data.
            If the answer cannot be determined from the data, please say so.
            
            Answer:""",
            input_variables=["context", "question"]
        )
        
        # Create the chain
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)
    
    def _create_context(self) -> str:
        """
        Create a string context from the loaded CSV documents.
        
        Returns:
            str: A formatted string containing the CSV data
        """
        context = []
        for doc in self.documents:
            context.append(doc.page_content)
        return "\n".join(context)
    
    def ask(self, question: str) -> str:
        """
        Ask a question about the CSV data.
        
        Args:
            question (str): The question to ask about the data
            
        Returns:
            str: The answer to the question
        """
        try:
            response = self.chain.invoke({
                "context": self.context,
                "question": question
            })
            return response["text"]
        except Exception as e:
            return f"Error processing question: {str(e)}"

# Example usage
if __name__ == "__main__":
    # Example with a sample CSV file
    file = os.path.abspath(r'..\data\all-course-list.csv')
    # Create the question answerer
    qa = CSVQuestionAnswerer(file)
    
    # Example questions
    questions = [
        "What is the total number of records in the dataset?",
        "What are the column names in the dataset?",
        "What is the course number for investments?",
        "What are the course numbers for investments and financial accounting?",
        "What courses are offered in Spring 2025?"
    ]
    
    # Test the question answerer
    for question in questions:
        print(f"\nQuestion: {question}")
        print(f"Answer: {qa.ask(question)}") 