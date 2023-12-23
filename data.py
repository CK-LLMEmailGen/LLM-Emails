

source = data.get("source")
destination = data.get("destination")
target = data.get("target")
prompt = data.get("prompt")

# Use the received values as needed, for example:
document_files = [source, destination]

# Load multiple documents
for file_path in document_files:
    loader = TextLoader(file_path)
    documents = loader.load()
    all_documents.extend(documents)

# Split the combined documents into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(all_documents)


