from   apps.config.database  import engine, SQLModel,create_contactlist_db,delete_contactlist_db,delete_all_contactlist,update_contactlist_db,create_contact_in_db
from fastapi import FastAPI,File
from apps.routes import contact,image,contactlist
from fastapi.staticfiles import StaticFiles
from apps.config.database import get_engine
from apps.core.core import CORSMiddleware,origins

#SQLModel.metadata.create_all(engine)
#create_contactlist_db()
#delete_contactlist_db()
#delete_all_contactlist()
#update_contactlist_db()
#create_contact_in_db()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
async def main():
    return {"message": "Hello World"}
app.include_router(contact.router,tags=["Contacts"])
app.mount("/static", StaticFiles(directory="apps/static"), name="static")
app.include_router(image.router,tags=["Images"])
app.include_router(contactlist.router,tags=["ContactLists"])


