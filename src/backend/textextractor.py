import os
from typing import List, Union
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.documents import Document



class DocumentLoader:
    """
    A flexible document loader that can handle both individual files
    and folders containing multiple files.
    """

    def __init__(self, path: str):
        """
        Initialize the DocumentLoader with a given file or folder path.

        Args:
            path (str): Path to a file or folder.
        """
        self.path: str = path
        

    def _load_file(self, file_path: str) -> List[Document]:
        """
        Load and extract content from a single PDF file.

        Args:
            file_path (str): Path to the PDF file.

        Returns:
            List[Document]: Extracted documents (per page).
        """
        print(f"Loading file: {file_path}")
        loader = PyMuPDFLoader(file_path, mode="page")
        return loader.load()

    def _load_folder(self, folder_path: str) -> List[Document]:
        """
        Load and extract content from all PDF files in a folder.

        Args:
            folder_path (str): Path to the folder.

        Returns:
            List[Document]: Combined list of extracted documents.
        """
        self.documents: List[Document] = []
        docs: List[Document] = []
        print(f"Loading all files from folder: {folder_path}")

        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)

            # Load only PDF files (you can extend this for more types)
            if file_path.lower().endswith(".pdf"):
                print(f" → Loading: {file_path}")
                docs.extend(self._load_file(file_path))
            else:
                print(f"Skipping non-PDF file: {file_path}")

        return docs

    def load(self) -> List[Document]:
        """
        Main method to load documents from the provided path.
        Automatically detects if the path is a file or folder.

        Returns:
            List[Document]: Extracted document objects.
        """
        if os.path.isfile(self.path):
            self.documents = self._load_file(self.path)
        elif os.path.isdir(self.path):
            self.documents = self._load_folder(self.path)
        else:
            raise ValueError("The provided path is neither a valid file nor a folder.")

        print(f"\n✅ Total documents loaded: {len(self.documents)}")
        return self.documents



