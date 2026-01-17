from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from ghl_client import get_opportunities, get_contacts

app = FastAPI(title="GHL → Excel API")


@app.get("/ghl/opportunities")
def opportunities(
    start_date: str = Query(None, description="YYYY-MM-DD"),
    end_date: str = Query(None, description="YYYY-MM-DD")
):
    data = get_opportunities(start_date, end_date)
    return JSONResponse(content=data)


@app.get("/ghl/contacts")
def contacts(
    start_date: str = Query(None, description="YYYY-MM-DD"),
    end_date: str = Query(None, description="YYYY-MM-DD")
):
    data = get_contacts(start_date, end_date)
    return JSONResponse(content=data)
