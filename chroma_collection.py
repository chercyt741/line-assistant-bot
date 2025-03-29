import os
import chromadb
from uuid import uuid4
chroma_client = chromadb.Client()

# switch `create_collection` to `get_or_create_collection` to avoid creating a new collection every time
collection = chroma_client.get_or_create_collection(name="funeral_articles")

input_folder="funeral_articles"


for filename in os.listdir(input_folder):
    if filename.endswith('.txt'):
        with open(os.path.join(input_folder, filename), 'r', encoding='utf-8') as f:
            content = f.read().strip()
        doc_id = str(uuid4())
        collection.upsert(documents=[content], ids=[doc_id])
        print(f"上傳：{filename}")

collection.add(
    documents=[
        "This is a document about funeral",
        "This is a document about prcoess",
        "This is a document about benefit",
        "This is a document about knowledge",
        "This is a document about custom",
    ],
    ids=["id1", "id2", "id3", "id4", "id5"],
)

results = collection.query(
    query_texts=["This is a query document about funeral"], # Chroma will embed this for you
    n_results=5 # how many results to return
)
print(results)