
from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import FastAPI, UploadFile, File, HTTPException
from pypdf import PdfReader

app = FastAPI(title="DocuMind AI")

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


@app.get("/")
def home():
    return {
        "message": "Welcome to DocuMind AI!",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/documents/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF file."
        )

    content = await file.read(MAX_FILE_SIZE + 1)

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="PDF must be 10 MB or smaller."
        )

    try:
        with NamedTemporaryFile(suffix=".pdf", delete=False) as temp:
            temp.write(content)
            temp_path = Path(temp.name)

        try:
            reader = PdfReader(str(temp_path))

            if reader.is_encrypted:
                raise HTTPException(
                    status_code=400,
                    detail="Encrypted PDFs are not supported yet."
                )

            pages = []

            for page_number, page in enumerate(reader.pages, start=1):
                text = page.extract_text() or ""
                pages.append({
                    "page": page_number,
                    "text": text
                })

            if not any(page["text"].strip() for page in pages):
                raise HTTPException(
                    status_code=400,
                    detail="No selectable text found in this PDF."
                )

            return {
                "filename": Path(file.filename).name,
                "total_pages": len(pages),
                "pages": pages
            }

        finally:
            temp_path.unlink(missing_ok=True)

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Could not read this PDF. Please check the file."
        )
    finally:
        await file.close()