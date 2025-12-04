import os
from pathlib import Path
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings


load_dotenv()

pinecone_api_key = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = "medical-ka-3-ai-assistant-index"

upload_dir = "./uploads"
os.makedirs(upload_dir, exist_ok=True)

# Connect to Pinecone (NO index creation anymore)
pc = Pinecone(api_key=pinecone_api_key)
index = pc.Index(PINECONE_INDEX_NAME)
print("Connected to existing Pinecone index:", PINECONE_INDEX_NAME)


def load_vectorstore(uploaded_files):
    embed_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2"
)

    file_paths = []
    print("Starting to save and process files...")

    # Save uploaded files
    for file in uploaded_files:
        save_path = Path(upload_dir) / file.filename
        with open(save_path, "wb") as f:
            f.write(file.file.read())
        file_paths.append(str(save_path))

    # Process files
    for file_path in file_paths:

        loader = PyPDFLoader(file_path)
        documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

        chunks = text_splitter.split_documents(documents)
        texts = [c.page_content for c in chunks]
          # Print first 2 texts for verification
        # SAFE metadata
        safe_metadatas = []
        for i, c in enumerate(chunks):
            safe_metadatas.append({
                "source": str(Path(file_path).name),  # only file name
                "page": int(c.metadata.get("page", 0)) if isinstance(c.metadata.get("page"), int) else 0,
                "chunk": i,
                "text": texts[i] # first 100 characters of the chunk
            })

        ids = [f"{Path(file_path).stem}_{i}" for i in range(len(texts))]

        # Convert embeddings to Python floats
        embeddings_list = embed_model.embed_documents(texts)
        embeddings_list = [list(map(float, emb)) for emb in embeddings_list]

        # Correct Pinecone vector format
        vectors = [
            {
                "id": ids[i],
                "values": embeddings_list[i],
                "metadata": safe_metadatas[i]
            }
            for i in range(len(ids))
        ]

        # print("Sample vector before upsert:")
        # print(vectors[0])

        index.upsert(vectors=vectors)

        print(f"Uploaded {len(vectors)} chunks from {file_path}")
