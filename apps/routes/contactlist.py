from fastapi import APIRouter, Depends,HTTPException
from typing import Annotated 
from sqlmodel import Session, select
from typing import List
from ..config.database import engine, get_engine
from ..models.models import Contact, ListContact
from ..schema.contactlist import contactlistRead, contactlistCreate, contactlistUpdate

router = APIRouter()    
@router.post("/create_listContact/", response_model=contactlistRead)
async def create_contact(contactlist: contactlistCreate,
                         session: Annotated[Session, 
                         Depends(get_engine)]):
        

        db_contactlist =    ListContact.model_validate(contactlist)
        session.add(db_contactlist)
        session.commit()
        session.refresh(db_contactlist)
        return db_contactlist

@router.get("/get_all_listContacts/", response_model=List[contactlistRead])
async def read_contactlist(session:Annotated[Session,Depends(get_engine)]): 
    if not session.exec(select(ListContact)).first():
        raise HTTPException(status_code=404, detail="No contact lists found")
    else:   
        contactlists = session.exec(select(ListContact)).all()
        return contactlists
    
@router.get("/get_listContact/{id}", response_model=contactlistRead)
async def read_contactlist_by_id(id:int, session:Annotated[Session,Depends(get_engine)]): 
    db_contactlist = session.get(ListContact, id)
    if not db_contactlist:
        raise HTTPException(status_code=404, detail="Contact list not found")    
    return db_contactlist

@router.post("/update_listContact/",response_model=contactlistRead,)  
async def update_contactlist(session:Annotated[Session,Depends(get_engine)],
                         id:int,
                         contactlist:contactlistUpdate):
        db_contactlist = session.get(ListContact, id)
        if not db_contactlist:
            raise HTTPException(status_code=404, detail="Contact list not found")
        contactlist_data = contactlist.model_dump(exclude_unset=True)
        for key, value in contactlist_data.items():
            setattr(db_contactlist, key, value)
        session.add(db_contactlist)
        session.commit()
        session.refresh(db_contactlist)
        return db_contactlist       

@router.get("/add_contact_to_contactlist/{id_list_contact}")
async def add_contact_to_list(id_contact:int,
                              id_list_contact:int,
                              session:Annotated[Session,Depends(get_engine)]):
    db_contact = session.get(Contact, id_contact)
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")  
    db_list_contact = session.get(ListContact, id_list_contact)
    if not db_list_contact:
        raise HTTPException(status_code=404, detail="Contact list not found")  
    db_contact.listContacts.append(db_list_contact)
    session.add(db_contact)
    session.commit()
    session.refresh(db_contact)
    return {"message": f"Contact {db_contact.name} added to list {db_list_contact.list_name}"}
 

@router.delete("/delete_listContact/")  
async def delete_contactlist(session:Annotated[Session,Depends(get_engine)],
                         id:int):
        db_contactlist = session.get(ListContact, id)
        if not db_contactlist:
            raise HTTPException(status_code=404, detail="Contact list not found")
        session.delete(db_contactlist)
        session.commit()
        return {"message": f"Contact list {db_contactlist.list_name} deleted successfully"}

@router.delete("/remove_contact_in_list_contact/{id_contact}")
async def delete_contact_in_listcontact(id_contact:int,
                                         id_list_contact:int,
                                         session:Annotated[Session,Depends(get_engine)]):
        contactlist= session.get(ListContact, id_list_contact)
        if not contactlist:
            raise HTTPException(status_code=404, detail="Contact not found")
        contact = session.get(Contact, id_contact)
        if not contact:
            raise HTTPException(status_code=404, detail="Contact list not found")
        if contact not in contactlist.contacts:
            raise HTTPException(status_code=400, detail="Contact not in the list")
        contactlist.contacts.remove(contact)
        session.add(contactlist)
        session.commit()
        session.refresh(contactlist)
        return {"message": f"Contact {contact.name} removed from list {contactlist.list_name}"}
