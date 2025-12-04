from fastapi import APIRouter, UploadFile, File
from typing import List
from modules.load_vectorstore import load_vectorstore
from fastapi.responses import JSONResponse
from logger import logger

router=APIRouter()



@router.post("/upload_pdfs")
async def upload_pdfs(files: List[UploadFile] = File(...)):
    try:
        print("Received files for upload:")
        load_vectorstore(files)
        logger.info("PDFs uploaded and processed successfully.")
        return JSONResponse(status_code=200, content={"message": "PDFs uploaded and processed successfully."})
    except Exception as e:
        logger.exception(f"Error: {e}")
        return JSONResponse(
            status_code=500,
            content={"message": f"Error: {str(e)}"}
        )
