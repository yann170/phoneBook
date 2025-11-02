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

   

class ContactCreate(ContactBase):
    pass    
    

class ContactUpdate(ContactBase):
    favorite: bool
    Blocked: bool

   

class ContactRead(ContactBase):
    id: int
    favorite: bool
    Blocked: bool

     
     
class ListContactRead(BaseModel):
    id: int
    list_name: str
    contacts: List[ContactRead] = []




        