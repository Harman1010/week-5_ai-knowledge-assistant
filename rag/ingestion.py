from pypdf import PdfReader

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from pathlib import Path

from utils.config import settings

def document_ingestion(file_path:str) -> list[Document]:

    """Processes the document and creates LangChain Document object having text as well as metadata"""

    reader = PdfReader(file_path)

    documents = []

    for page_number , page in enumerate(reader.pages,start=1):

        text = page.extract_text() or ""

        if text.strip():
            documents.append(Document(
                page_content = text,
                metadata = {
                    "source" : Path(file_path).name,
                    "page" : page_number
                }
            ))

    return documents

def chunking(documents : list[Document]) -> list[Document]:

    """Splitting the document into chunks for better retrieval and staying within the model's context window"""

    splitter = RecursiveCharacterTextSplitter(chunk_size=settings.chunk_size,chunk_overlap=settings.chunk_overlap)

    return splitter.split_documents(documents)