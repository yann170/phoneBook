from pydantic import BaseModel
from typing import List
from sqlmodel import SQLModel
from ..models.models import Contact, ListContact


class ContactBase(SQLModel):
    name: str
    email: str
    phone: str
    address: str
    company: str  
    image_url: str | None = None 
    listContacts: List[ListContact] = []
    favorite: bool | None = False 
    Blocked: bool   | None = False

   

class ContactCreate(ContactBase):
    pass  
    

class ContactUpdate(ContactBase):
    pass
   

   

class ContactRead(SQLModel):
    id: int
    name: str
    email: str
    phone: str
    address: str
    image_url : str
    favorite : bool
    Blocked : bool
    
     
     
class ListContactRead(BaseModel):
    id: int
    list_name: str
    contacts: List[ContactRead] = []




        