import json
from chromadb import PersistentClient
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
client = PersistentClient(path="db")

# Create a collection to store the data
collection = client.create_collection(
    os.getenv("COLLECTION_NAME"), embedding_function=ef
)

# Loop through each data point
for idx, d in enumerate(data):
    # Save the metadata
    metadata = {k: ",".join(v) if isinstance(v, list) else v for k, v in d.items()}

    print(f"Adding data point {idx}: {metadata}")

    try:
        # Add to the collection
        collection.add(
            ids=[str(idx)],
            embeddings=None,
            metadatas=[metadata],
            documents=[d["code"]],
        )
        print(f"Data point {idx} added successfully.")
    except ValueError as e:
        print(f"Error adding data point {idx}: {e}")
    except Exception as e:
        print(f"Unexpected error adding data point {idx}: {e}")
