from logger import logger

def query_chain(chain, user_input: str):
    try:
        logger.debug(f"Received user input: {user_input}")

        # LCEL call → returns dict {"answer": "...", "docs": [...]}
        result = chain.invoke(user_input)
        docs = result["docs"]

        # for i, doc in enumerate(docs):
        #     print(f"\n---- Document {i} ----")
        #     print(doc.metadata)

       

        response = {
            "response": result["answer"],
            "source_documents": [
                doc.metadata.get("source", "") if doc.metadata else ""
                for doc in result.get("docs", [])
            ]
        }

        logger.debug(f"Generated response: {response}")
        return response

    except Exception as e:
        logger.error(f"Error running chain: {e}")
        raise e
