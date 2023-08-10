import json
from chromadb import Client
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load the data
with open("code_data.json") as f:
    data = json.load(f)

# Instantiate the EmbeddingFunction
ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.getenv("OPENAI_API_KEY"), model_name="text-embedding-ada-002"
)

# Create a ChromaDB client and pass the ef
client = Client(
    Settings(chroma_db_impl="duckdb+parquet", persist_directory="db")
)

# Create a collection to store the data
collection = client.create_collection("code_snippets", embedding_function=ef)

# Loop through each data point
for idx, d in enumerate(data):
    # Save the metadata
    metadata = {
        k: ",".join(v) if isinstance(v, list) else v for k, v in d.items()
    }

    print(f"Adding data point {idx}: {metadata}")

    try:
        # Add to the collection
        collection.add(
            ids=[str(idx)],
            embeddings=None,
            metadatas=[metadata],
            documents=[d["code"]],
            increment_index=True,
        )
        print(f"Data point {idx} added successfully.")
    except ValueError as e:
        print(f"Error adding data point {idx}: {e}")
    except Exception as e:
        print(f"Unexpected error adding data point {idx}: {e}")

# Persist the data on disk
client.persist()
