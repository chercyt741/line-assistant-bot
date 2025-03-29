from chromadb.config import Settings
from chromadb import Client

# Initialize the Chroma client with persistence
client = Client(Settings(persist_directory="./chroma"))

# Access the collection
collection = client.get_or_create_collection("funeral_articles")

# Print all document IDs
print(collection.get()['ids'])

# Perform a query
results = collection.query(query_texts=["靈骨塔方位推薦？"], n_results=3)
print(results)