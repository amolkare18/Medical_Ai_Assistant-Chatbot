from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from pinecone import Pinecone
from pydantic import Field
from typing import List, Optional
from logger import logger
from langchain_huggingface import HuggingFaceEmbeddings
import os

from modules.llm import get_llm_chain
from modules.query_handlers import query_chain

router = APIRouter()


class SimpleRetriever(BaseRetriever):
    docs: List[Document] = Field(default_factory=list)

    def _get_relevant_documents(self, query: str) -> List[Document]:
        """Return all documents retrieved from Pinecone."""
        return self.docs

    async def _aget_relevant_documents(self, query: str) -> List[Document]:
        return self.docs


@router.post("/ask")
async def ask_question(question: str = Form(...)):
    try:
        logger.info(f"Received question: {question}")

        # Load environment variables safely
        pinecone_api_key = os.environ["PINECONE_API_KEY"]
        pinecone_index_name = os.environ["PINECONE_INDEX_NAME"]

        # Initialize Pinecone
        pc = Pinecone(api_key=pinecone_api_key)
        index = pc.Index(name=pinecone_index_name)

        # Embedding model
        embed_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-mpnet-base-v2"
            )
        embedded_query = embed_model.embed_query(question)

        # Pinecone query
        result = index.query(
            vector=embedded_query,
            top_k=3,
            include_metadata=True
        )

        # Convert Pinecone matches → LangChain Documents
        docs = [
            Document(
                page_content=match["metadata"].get("text", ""),
                metadata=match["metadata"]
            )
            for match in result.get("matches", [])
        ]

        # print("Retrieved documents:", docs)

        # Create retriever
        retriever = SimpleRetriever(docs=docs)

        # Build LLM chain
        llm_chain = get_llm_chain(retriever)

        # Run final chain
        response = query_chain(llm_chain, user_input=question)

        logger.info("Generated response successfully.")
        return JSONResponse(status_code=200, content=response)

    except Exception as e:
        logger.exception(f"Error: {e}")
        return JSONResponse(
            status_code=500,
            content={"message": "An error occurred while processing your question."},
        )
