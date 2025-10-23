from  sqlmodel import SQLModel, Field,Relationship
from datetime import datetime, timezone


class ContactListLink(SQLModel, table=True):
    contact_id: int = Field(default= int,foreign_key="contact.id", primary_key=True)
    list_id: int = Field(default=None,foreign_key="listcontact.id", primary_key=True) 

class Contact(SQLModel, table=True):
    id:  int  = Field(default=None, primary_key=True)
    name: str
    email: str | None = None
    phone: str | None = None
    address: str | None = None
    company: str | None = None
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
        nullable=False)
    listContacts: list["ListContact"] = Relationship(back_populates="contacts", link_model=ContactListLink)
    favorite: bool = Field(default=False)
    Blocked: bool = Field(default=False)
    image_url: str | None = None
  
 
class ListContact(SQLModel, table=True):
    id: int  = Field(default=None, primary_key=True)
    list_name: str = Field(index=True,unique=True)
    contacts: list[Contact] = Relationship(back_populates="listContacts", link_model=ContactListLink)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
        nullable=False)


    