from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

# text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 200)

class chunking:
    def __init__(self,docs, chunk_size: int = 1000, chunk_overlap: int = 200, ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", ".", "!", "?", " "]
        )
        self.docs = docs
        
    def chunker(self):
# If docs is a list of Document-like objects, use split_documents.
        try:
            if isinstance(self.docs, list) and len(self.docs) > 0 and hasattr(self.docs[0], 'page_content'):
                self.chunks = self.splitter.split_documents(self.docs)
            else:
                # If docs is a single string or a list of strings, convert to a single string and split.
                text = self.docs if isinstance(self.docs, str) else '\n'.join(self.docs)
                self.chunks = self.splitter.split_text(text)
            return self.chunks
        except Exception as e:
            print(Exception)

# if __name__ == "__main__":
#     chunker = chunking(docs= docs)
#     chunks = chunker.chunker()
#     print(f"Produced {len(chunks)} chunks")
#     # preview first chunk
#     chunks[:50]