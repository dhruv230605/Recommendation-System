from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_models import AzureChatOpenAI
from langchain.prompts import PromptTemplate
import json
import os
from typing import List, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class TransactionAssistant:
    def __init__(self):
        """
        Initialize the Transaction Assistant with necessary components.
        """
        # Get Azure OpenAI credentials from environment variables
        openai_api_key = os.getenv("OPENAI_API_KEY")
        openai_api_base = os.getenv("OPENAI_DEPLOYMENT_ENDPOINT")
        deployment_name = os.getenv("OPENAI_DEPLOYMENT_NAME", "gpt-4o-mini")
        
        if not all([openai_api_key, openai_api_base]):
            raise ValueError("OPENAI_API_KEY and OPENAI_DEPLOYMENT_ENDPOINT environment variables must be set")
            
        # Store credentials
        self.openai_api_key = openai_api_key
        self.openai_api_base = openai_api_base.rstrip('/') 
        
        # Initialize the embedding model
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        # Connect to the existing ChromaDB vector store
        self.vectorstore = Chroma(
            persist_directory="./chroma_db",
            embedding_function=self.embeddings,
            collection_name="financial_data"
        )
        
        try:
            # Initialize the Azure OpenAI chat model
            self.llm = AzureChatOpenAI(
                openai_api_version="2023-05-15",
                azure_deployment=deployment_name,
                azure_endpoint=self.openai_api_base,
                api_key=openai_api_key,
                temperature=0.7 
            )
        except Exception as e:
            raise ValueError(f"Failed to initialize Azure OpenAI model. Please check your credentials. Error: {str(e)}")
        
        # Initialize conversation memory to maintain chat history
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # Create the conversational chain for Q&A
        self.qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vectorstore.as_retriever(),
            memory=self.memory,
            combine_docs_chain_kwargs={"prompt": self._get_qa_prompt()}
        )

    def _get_qa_prompt(self) -> PromptTemplate:
        """
        Create a custom prompt template for the QA chain.
        This template guides how the model should respond to questions.
        """
        template = """You are a helpful financial assistant specializing in transaction analysis. 
        Use the following pieces of context to answer the question at the end.
        If you don't know the answer, just say that you don't know, don't try to make up an answer.

        Context: {context}

        Chat History: {chat_history}
        Human: {question}
        Assistant:"""
        
        return PromptTemplate(
            input_variables=["context", "chat_history", "question"],
            template=template
        )

    def get_transaction_recommendations(self, user_id: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get personalized offers and strategies based on user's transaction history.
        
        Args:
            user_id (str): The ID of the user to get recommendations for
            
        Returns:
            Dict containing offers and strategies based on user's transaction patterns
        """
        # Step 1: Get user's recent transactions
        user_transactions = self.vectorstore.similarity_search(
            f"user_id: {user_id}",
            k=5,  # Get 5 most recent transactions
            filter={"record_type": "transaction"}
        )
        
        # Step 2: Extract categories from transactions
        categories = [doc.metadata.get("category", "") for doc in user_transactions]
        
        # Step 3: Find relevant offers based on transaction categories
        offers = self.vectorstore.similarity_search(
            f"categories: {', '.join(categories)}",
            k=3,  # Get top 3 matching offers
            filter={"record_type": "offer"}
        )
        
        # Step 4: Get investment strategies based on spending patterns
        strategies = self.vectorstore.similarity_search(
            f"spending patterns: {', '.join(categories)}",
            k=2,  # Get top 2 matching strategies
            filter={"record_type": "investment_strategy"}
        )
        
        return {
            "offers": [doc.metadata for doc in offers],
            "strategies": [doc.metadata for doc in strategies]
        }

    def chat(self, question: str) -> str:
        """
        Handle transaction-related queries using the conversational chain.
        
        Args:
            question (str): The user's question about transactions
            
        Returns:
            str: The assistant's response
        """
        response = self.qa_chain({"question": question})
        return response["answer"]

# Example
if __name__ == "__main__":
    try:
        
        assistant = TransactionAssistant()
        
       
        # user_id = "40f2a9c5-ca1d-4269-99cc-a2e9774d490b"
        # transaction_recs = assistant.get_transaction_recommendations(user_id)
        # print("Transaction Recommendations:", transaction_recs)
        
        
        response = assistant.chat("What is my largest value transaction?")
        print("Chat Response:", response)
    except ValueError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}") 