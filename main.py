from fastapi import FastAPI
from fastapi.responses import JSONResponse
from ghl_client import get_opportunities, get_contacts

app = FastAPI(title="GHL API")

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/ghl/opportunities")
def opportunities():
    return JSONResponse(content=get_opportunities())

@app.get("/ghl/contacts")
def contacts():
    return JSONResponse(content=get_contacts())
