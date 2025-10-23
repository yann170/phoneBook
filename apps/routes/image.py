from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from typing import Annotated
from sqlmodel import Session
from apps.config.database import get_engine
from apps.models.models import Contact
import uuid
import os

router = APIRouter()
@router.post("/upload_image/")
async def upload_image(id_contact:int ,
                       session: Annotated[Session,  Depends(get_engine)],
                       file: UploadFile = File(...)):
    
    db_contact = session.get(Contact, id_contact)  
    uuid_image = str(uuid.uuid4())
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    contact_data_image = db_contact.image_url
    if contact_data_image:
        image_location = f"apps/static/{uuid_image}.jpg"
        if os.path.exists(contact_data_image):
            os.remove(contact_data_image)
        db_contact.image_url = image_location          
        session.add(db_contact)
        session.commit()
        session.refresh(db_contact)
        with open(image_location, "wb+") as file_object:
            file_object.write(file.file.read())
        return {"info": f"file '{file.filename}' saved at '{image_location}"}

@router.get("/get_image/{id_contact}")
async def get_image(id_contact:int ,
                    session: Annotated[Session,  Depends(get_engine)]):
    
    db_contact = session.get(Contact, id_contact)  
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    contact_data_image = db_contact.image_url
    if not contact_data_image:
        raise HTTPException(status_code=404, detail="Image not found") 
    if os.path.exists(contact_data_image):
        return FileResponse(contact_data_image)
    else:
        raise HTTPException(status_code=404, detail="Image file does not exist")