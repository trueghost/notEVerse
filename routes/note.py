from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from models.note import Note
from bson import ObjectId
from config.db import conn
from schemas.note import noteEntity, notesEntity
from fastapi.responses import RedirectResponse

note = APIRouter()
templates = Jinja2Templates(directory="templates")

@note.delete("/delete/{note_id}")
async def delete_note(note_id: str):
    result = conn.notes.notes.delete_one({"_id": ObjectId(note_id)})

    if result.deleted_count == 1:
        # Redirect back to the homepage ("/") after successful deletion
        return RedirectResponse(url="/", status_code=303)
    else:
        return {"message": "Note not found"}

@note.get("/", response_class=HTMLResponse)
async def read_note(request: Request):
    action = request.query_params.get("action")
    if action == "delete":
        note_id = request.query_params.get("note_id")
        # Delete the note based on the note_id
        result = conn.notes.notes.delete_one({"_id": ObjectId(note_id)})
        if result.deleted_count == 1:
            # Redirect back to the homepage ("/") after successful deletion
            return RedirectResponse(url="/", status_code=303)
        else:
            return {"message": "Note not found"}
    else:
        docs = conn.notes.notes.find({})
        newDocs = []
        for doc in docs:
            newDocs.append({
                "id": str(doc["_id"]),
                "title": doc["title"],
                "desc": doc["desc"],
                "important": doc["important"],
            })
        return templates.TemplateResponse("index.html", {"request": request, "newDocs": newDocs})

@note.post("/")
async def add_note(request: Request):
    form = await request.form()
    formDict = dict(form)
    formDict["important"] = True if formDict.get("important") == "on" else False # type: ignore
    note = conn.notes.notes.insert_one(formDict)
    # Redirect to the same page
    return RedirectResponse(url=request.url, status_code=303)

@note.get("/edit/{note_id}", response_class=HTMLResponse)
async def edit_note_form(request: Request, note_id: str):
    note = conn.notes.notes.find_one({"_id": ObjectId(note_id)})
    if note:
        return templates.TemplateResponse("edit.html", {"request": request, "note": note, "note_id": note_id})
    else:
        return {"message": "Note not found"}

@note.post("/edit/{note_id}")
async def edit_note(note_id: str, request: Request):
    form = await request.form()
    formDict = dict(form)
    formDict["important"] = True if formDict.get("important") == "on" else False # type: ignore
    result = conn.notes.notes.update_one({"_id": ObjectId(note_id)}, {"$set": formDict})

    if result.modified_count == 1:
        return RedirectResponse(url="/", status_code=303)
    