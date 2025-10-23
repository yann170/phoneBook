from sqlmodel import create_engine, SQLModel, Session,select
from apps.models.models import Contact, ListContact, ContactListLink


sqlite_file_name = "dataPhonebook.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True)



def create_contactlist_db():
     with Session(engine) as session:
        team_preventers = ListContact(list_name="icloud8")   
        session.add(team_preventers)
        session.commit()
        session.refresh(team_preventers)

        print("icloud contact list created:",team_preventers.id ,"et" ,team_preventers.list_name)

def delete_contactlist_db():
     with Session(engine) as session:
        icloud_listcontact = session.exec(
            select(ListContact).where(ListContact.list_name == "icloud4")
        ).all()
        for icloud_listcontact in icloud_listcontact:
            session.delete(icloud_listcontact)
            session.commit()  
        print("icloud contact list deleted")  

def delete_all_contactlist():
        with Session(engine) as session:
            all_listcontact = session.exec(
                select(ListContact)
            ).all()
            for all_listcontact in all_listcontact:
                session.delete(all_listcontact)
                session.commit()  
            print("all contact lists deleted")

def create_contact_in_db():
     with Session(engine) as session:
        new_contact = Contact(name="John", email="yann", phone="1234567890")   
        session.add(new_contact)
        session.commit()
        session.refresh(new_contact)
        print("Contact created:",new_contact.id ,"et" ,new_contact.name)

def update_contactlist_db():
     with Session(engine) as session:
        icloud_listcontact = session.exec(
            select(ListContact).where(ListContact.list_name == "icloud2")
        ).first()
        if icloud_listcontact:
            icloud_listcontact.list_name = "icloud5"
            icloud_listcontact.id = 7
            session.add(icloud_listcontact)
            session.commit()  
            session.refresh(icloud_listcontact)
            print("icloud contact list updated:",icloud_listcontact.id ,"et" ,icloud_listcontact.list_name)
        else:
            print("icloud contact list not found")

def get_engine():
    with Session(engine) as session:
        yield session    