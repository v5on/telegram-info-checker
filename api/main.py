from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Limit it to your Vercel domain later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPSTREAM_BASE_URL = "tele-user-info-api-production.up.railway.app"

@app.get("/api/check")
async def check_phones(phones: str = Query(...)):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{UPSTREAM_BASE_URL}/check", params={"phones": phones})
        return JSONResponse(content=resp.json(), status_code=resp.status_code)

@app.get("/api/get_user_info")
async def get_user_info(username: str = Query(...)):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{UPSTREAM_BASE_URL}/get_user_info", params={"username": username})
        return PlainTextResponse(content=resp.text, status_code=resp.status_code)
