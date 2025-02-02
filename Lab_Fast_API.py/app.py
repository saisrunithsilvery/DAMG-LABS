from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool | None = None

@app.get("/")
def read_root():
    return {"Message": "First API"}
    
@app.post("/item/")
def create_item(item: Item):
    return item

@app.get("/items/{item_id}")
def read_item(item_id: int, name: str | None = None):
    return {"item_id": item_id, "name": name}

@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        # Check if a file was actually uploaded
        if not file:
            raise HTTPException(status_code=400, detail="No file uploaded")

        # Check if the uploaded file is a PDF
        if not file.content_type == 'application/pdf':
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")

        # Create the uploads directory if it doesn't exist
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)

        # Save the uploaded PDF file
        file_location = os.path.join(upload_dir, file.filename)
        
        # Read the file in chunks for better memory handling
        try:
            contents = await file.read()
            with open(file_location, "wb") as f:
                f.write(contents)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

        return JSONResponse(
            status_code=200,
            content={
                "filename": file.filename,
                "message": "PDF uploaded successfully!"
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))