from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_core.runnables import RunnableMap, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import os
from operator import itemgetter
from dotenv import load_dotenv

load_dotenv()

def get_llm_chain(retriever):
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        groq_api_key=os.getenv("GROQ_API_KEY")
    )

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=(
            "Use the following context to answer the question.\n"
            "If unknown, don't say you don't know. find the similar words from question in context \n\n"
            "Context:\n{context}\n\n"
            "Question:\n{question}\n\n"
            "Answer:"
        )
    )

    # Final LCEL chain that returns answer AND docs
    chain = (
        RunnableMap({
            "context": retriever,          # calls retriever → returns list[Document]
            "question": RunnablePassthrough()
        })
        | RunnableMap({
            "answer": prompt | llm | StrOutputParser(),
             "docs": itemgetter("context"),  # forward docs
        })
    )

    return chain
