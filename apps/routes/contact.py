from fastapi import APIRouter, Depends,HTTPException
from typing import Annotated 
from sqlmodel import Session, select
from typing import List
from ..config.database import engine, get_engine
from ..models.models import Contact, ListContact
from ..schema.contact import ContactRead, ContactCreate, ContactUpdate




router = APIRouter()
 
@router.post("/create_contact/", response_model=ContactRead)
async def create_contact(contact: ContactCreate, id_contactList : int ,
                         session: Annotated[Session, 
                         Depends(get_engine)]):
     contact_list = session.get(ListContact, id_contactList)
     if contact_list is None:
            raise HTTPException(status_code=404, detail="Contact list not found")
     else:
        contact.listContacts.append(contact_list)
        db_contact = Contact.model_validate(contact)
        session.add(db_contact)
        session.commit()
        session.refresh(db_contact)
        return db_contact
    
@router.get("/get_all_contacts/", response_model=List[ContactRead])
async def read_contact(session:Annotated[Session,Depends(get_engine)]): 
    if not session.exec(select(Contact)).first():
        raise HTTPException(status_code=404, detail="No contacts found")
    else:   
        contacts = session.exec(select(Contact)).all()
        return contacts

@router.get("/get_Contacts/{id}", response_model=ContactRead)
async def read_contact_by_id(id:int, session:Annotated[Session,Depends(get_engine)]): 
    db_contact = session.get(Contact, id)
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")    
    return db_contact
    
@router.post("/upgate_Contact/",response_model=ContactUpdate)  
async def update_contact(session:Annotated[Session,Depends(get_engine)],
                         id:int,
                         contact:ContactUpdate):
        db_contact = session.get(Contact, id)
        if not db_contact:
            raise HTTPException(status_code=404, detail="Contact not found")
        contact_data = contact.model_dump(exclude_unset=True)
        for key, value in contact_data.items():
            setattr(db_contact, key, value)
        session.add(db_contact)
        session.commit()
        session.refresh(db_contact)
        return db_contact

@router.get("/add_contact_to_list/{id_list_contact}")
async def add_contact_to_list(id_contact:int,
                              id_list_contact:int,
                              session:Annotated[Session,Depends(get_engine)]):
        contact = session.get(Contact, id_contact)
        if not contact:
            raise HTTPException(status_code=404, detail="Contact not found")
        list_contact = session.get(ListContact, id_list_contact)
        if not list_contact:
            raise HTTPException(status_code=404, detail="Contact list not found")
        if list_contact in contact.listContacts:
            raise HTTPException(status_code=400, detail="Contact already in the list")
        contact.listContacts.append(list_contact)
        session.add(contact)
        session.commit()
        session.refresh(contact)
        return {"message": f"Contact {contact.name} added to list {list_contact.list_name}"}

@router.delete("/delete_Contact/",response_model=ContactRead)  
async def delete_contact(session:Annotated[Session,Depends(get_engine)],
                         id:int):
        db_contact = session.get(Contact, id)
        if not db_contact:
            raise HTTPException(status_code=404, detail="Contact not found")
        session.delete(db_contact)
        session.commit()
        return db_contact

@router.delete("/remove_list_contact_in_contact/{id_list_contact}")
async def delete_contact_in_listcontact(id_contact:int,
                                         id_list_contact:int,
                                         session:Annotated[Session,Depends(get_engine)]):
        contact = session.get(Contact, id_contact)
        if not contact:
            raise HTTPException(status_code=404, detail="Contact not found")
        list_contact = session.get(ListContact, id_list_contact)
        if not list_contact:
            raise HTTPException(status_code=404, detail="Contact list not found")
        if list_contact not in contact.listContacts:
            raise HTTPException(status_code=400, detail="Contact not in the list")
        contact.listContacts.remove(list_contact)
        session.add(contact)
        session.commit()
        session.refresh(contact)
        return {"message": f"Contact {contact.name} removed from list {list_contact.list_name}"}

  

@router.get("/get_all_favorite_contact/", response_model=List[ContactRead])
async def read_contact_favorite(session:Annotated[Session,Depends(get_engine)]): 

    if not session.exec(select(Contact)).first():
        raise HTTPException(status_code=404, detail="No favorite contacts found")
    else:   
        contacts_favorite = session.exec(select(Contact).where(Contact.favorite==True)).all()
        return contacts_favorite