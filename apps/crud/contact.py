from typing import Annotated
from fastapi import Depends,HTTPException
from sqlmodel import Session, select
from ..models.models import ListContact,Contact
from ..config.database import engine, get_engine


def verified_contact(id: int, session: Annotated[Session, Depends(get_engine)]):
    contact = session.get(Contact, id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return True

def verified_listcontact(id_list_contact: int, session: Annotated[Session, Depends(get_engine)]):
    list_contact = session.get(ListContact, id_list_contact)
    if not list_contact:
        raise HTTPException(status_code=404, detail="Contact list not found")
    return list_contact