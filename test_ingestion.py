from rag.ingestion import document_ingestion , chunking

file_path = ""

def main():

    documents = document_ingestion(file_path)

    chunks = chunking(documents)

    print("Pages:",len(documents))

    print("Chunks size",len(chunks))

    for i , chunk in enumerate(chunks[:3]):

        print(f"Chunk {i}")
        print(f"Metadata:",chunk.metadata)
        print("Text:",chunk.page_content[:300])


if __name__ == "__main__":

    main()