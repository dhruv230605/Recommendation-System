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
        
        openai_api_key = os.getenv("OPENAI_API_KEY")
        openai_api_base = os.getenv("OPENAI_DEPLOYMENT_ENDPOINT")
        deployment_name = os.getenv("OPENAI_DEPLOYMENT_NAME", "gpt-4o-mini")
        
        if not all([openai_api_key, openai_api_base]):
            raise ValueError("OPENAI_API_KEY and OPENAI_DEPLOYMENT_ENDPOINT environment variables must be set")
            
        # storing
        self.openai_api_key = openai_api_key
        self.openai_api_base = openai_api_base.rstrip('/') 
        
        #embedding model
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        # existing vdb from chroma
        self.vectorstore = Chroma(
            persist_directory="./chroma_db",
            embedding_function=self.embeddings,
            collection_name="financial_data"
        )
        
        try:
            # Initialize model
            self.llm = AzureChatOpenAI(
                openai_api_version="2023-05-15",
                azure_deployment=deployment_name,
                azure_endpoint=self.openai_api_base,
                api_key=openai_api_key,
                temperature=0.7 
            )
        except Exception as e:
            raise ValueError(f"Failed, Error: {str(e)}")
        
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
        template = """You are a helpful financial assistant specializing in transaction analysis. 
        Use the following pieces of context to answer the question at the end.
        get_transaction_recommendations is a function that takes a user_id as input and returns a list of offers and strategies. Only use this function if the user asks for recommendations.
        Only consider transactions that belong to the user ID mentioned in the question.
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
        
        user_transactions = self.vectorstore.similarity_search(
            f"user_id: {user_id}",
            k=5, 
            filter={"record_type": "transaction"}
        )
        
        categories = [doc.metadata.get("category", "") for doc in user_transactions]
        
        
        offers = self.vectorstore.similarity_search(
            f"categories: {', '.join(categories)}",
            k=3, 
            filter={"record_type": "offer"}
        )
        
        
        strategies = self.vectorstore.similarity_search(
            f"spending patterns: {', '.join(categories)}",
            k=2, 
            filter={"record_type": "investment_strategy"}
        )
        
        
        offer_details = []
        for doc in offers:
            metadata = doc.metadata
            try:
                discount_value = json.loads(metadata.get("discount_value", "{}"))
            except:
                discount_value = {}
                
            offer_data = {
                "name": metadata.get("name", "Unnamed Offer"),
                "description": metadata.get("description", "No description available"),
                "type": metadata.get("type", "Unknown type"),
                "discount_value": discount_value,
                "applicable_categories": metadata.get("applicable_categories", "").split(", "),
                "minimum_transaction_amount": metadata.get("minimum_transaction_amount", 0)
            }
            offer_details.append(offer_data)
        
        
        strategy_details = []
        for doc in strategies:
            metadata = doc.metadata
            try:
                allocation_blueprint = json.loads(metadata.get("allocation_blueprint", "{}"))
                performance_metrics = json.loads(metadata.get("performance_metrics", "{}"))
            except:
                allocation_blueprint = {}
                performance_metrics = {}
                
            strategy_data = {
                "name": metadata.get("name", "Unnamed Strategy"),
                "risk_profile": metadata.get("risk_profile", "Not specified"),
                "time_horizon": metadata.get("time_horizon", "Not specified"),
                "target_annual_return": metadata.get("target_annual_return", 0),
                "allocation_blueprint": allocation_blueprint,
                "performance_metrics": performance_metrics
            }
            strategy_details.append(strategy_data)
        
        return {
            "offers": offer_details,
            "strategies": strategy_details
        }

    def chat(self, question: str) -> str:
        
        user_id = None
        if "user id is" in question.lower():
            user_id = question.lower().split("user id is")[1].split()[0].strip()
        
        
        recommendations = None
        if "recommendations" in question.lower() and user_id:
            recommendations = self.get_transaction_recommendations(user_id)
        
        
        response = self.qa_chain({"question": question})
        answer = response["answer"]
        
        
        if recommendations:
            answer += "\n\nPersonalized Recommendations:\n"
            
            if recommendations["offers"]:
                answer += "\nOffers for you:\n"
                for offer in recommendations["offers"]:
                    answer += f"- {offer['name']}: {offer['description']}\n"
                    answer += f"  Type: {offer['type']}, "
                    if offer['discount_value']:
                        discount = offer['discount_value']
                        answer += f"Discount: {discount.get('value', '')}{discount.get('type', '')}, "
                    answer += f"Min. Amount: ₹{offer['minimum_transaction_amount']}\n"
            
            if recommendations["strategies"]:
                answer += "\nInvestment Strategies:\n"
                for strategy in recommendations["strategies"]:
                    answer += f"- {strategy['name']}\n"
                    answer += f"  Risk Profile: {strategy['risk_profile']}, "
                    answer += f"Time Horizon: {strategy['time_horizon']}, "
                    answer += f"Target Return: {strategy['target_annual_return']}%\n"
                    if strategy['allocation_blueprint']:
                        answer += "  Allocation: "
                        allocations = [f"{k}: {v}%" for k, v in strategy['allocation_blueprint'].items()]
                        answer += ", ".join(allocations) + "\n"
        
        return answer


if __name__ == "__main__":
    try:
        
        assistant = TransactionAssistant()
        
       
        user_id = "40f2a9c5-ca1d-4269-99cc-a2e9774d490b"
        transaction_recs = assistant.get_transaction_recommendations(user_id)
        print("Transaction Recommendations:", transaction_recs)
        
        
        response = assistant.chat('''What categories am I buying from? My user id is 40f2a9c5-ca1d-4269-99cc-a2e9774d490b. 
                                  Suggest me recommendations for my transaction history.
                                  Also have I made any other transactions?''')
        print("Chat Response:", response)
    except ValueError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}") 