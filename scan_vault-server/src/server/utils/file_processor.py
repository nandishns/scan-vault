from typing import Optional
import pdfplumber
import pandas as pd
from io import BytesIO
import logging

logger = logging.getLogger(__name__)

class FileProcessor:
    """Utility class for processing different file types."""

    SUPPORTED_EXTENSIONS = {
        "txt": "text",
        "pdf": "pdf",
        "csv": "csv",
        "docx": "docx",
        "jpg": "image",
        "jpeg": "image",
        "png": "image",
        "bmp": "image"
    }

    async def process_file(self, file, file_extension: str) -> Optional[str]:
        """Process file based on its extension."""
        if file_extension not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(f"Unsupported file type: {file_extension}")

        processors = {
            "txt": self._process_text,
            "pdf": self._process_pdf,
            "csv": self._process_csv,
            "docx": self._process_docx
        }

        processor = processors.get(file_extension)
        if not processor:
            raise ValueError(f"No processor found for {file_extension}")

        return await processor(file)

    def get_file_extension(self, filename: str) -> str:
        """Extract and validate file extension."""
        try:
            extension = filename.split(".")[-1].lower()
            if extension not in self.SUPPORTED_EXTENSIONS:
                raise ValueError(f"Unsupported file type: {extension}")
            return extension
        except Exception as e:
            logger.error(f"Error extracting file extension: {e}")
            raise ValueError("Invalid filename")

    async def _process_text(self, file) -> str:
        """Process text file."""
        content = await file.read()
        return content.decode("utf-8")

    async def _process_pdf(self, file) -> str:
        """Process PDF file."""
        content = []
        with pdfplumber.open(file.file) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    content.append(text)
        return " ".join(content)

    async def _process_csv(self, file) -> str:
        """Process CSV file."""
        content = await file.read()
        df = pd.read_csv(BytesIO(content))
        return df.to_string(index=False)

    async def _process_docx(self, file) -> str:
        """Process DOCX file."""
        from docx import Document
        content = await file.read()
        doc = Document(BytesIO(content))
        return " ".join([para.text for para in doc.paragraphs]) 