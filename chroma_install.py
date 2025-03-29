import os
import chromadb

# Setup Chroma in-memory, for easy prototyping. Can add persistence easily!
client = chromadb.Client()

# Create collection. get_collection, get_or_create_collection, delete_collection also available!
collection = client.create_collection("all-my-documents")

# Path to the directory containing the files
directory_path = "funeral_articles"  # Ensure this is the directory path

# Iterate through all files in the directory
for filename in os.listdir(directory_path):
    file_path = os.path.join(directory_path, filename)

    # Skip directories, only process files
    if os.path.isfile(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                file_content = file.read()  # Read the entire content of the file

            # Add the file content to the collection
            collection.add(
                documents=[file_content],  # Add the file content as a document
                metadatas=[{"source": filename}],  # Metadata for filtering
                ids=[filename],  # Use the filename as the unique ID
            )
            print(f"Added file '{filename}' to the collection.")
        except Exception as e:
            print(f"Error processing file '{filename}': {e}")

# Query/search 2 most similar results. You can also .get by id
results = collection.query(
    query_texts=["This is a query document"],
    n_results=2,
)

# Print the query results
print("Query Results:")
print(results)