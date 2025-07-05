from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI()

origins = ["*"]  # You can limit to Vercel domain if needed

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Replace this with your real backend URL (but don't expose it in frontend)
BACKEND_URL = "https://tele-user-info-api-production.up.railway.app"

@app.get("/check")
async def check_phones(phones: str = Query(...)):
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{BACKEND_URL}/check", params={"phones": phones})
        return JSONResponse(content=r.json(), status_code=r.status_code)

@app.get("/get_user_info")
async def get_user_info(username: str = Query(...)):
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{BACKEND_URL}/get_user_info", params={"username": username})
        return JSONResponse(content=r.json() if r.status_code == 200 else {"error": r.text}, status_code=r.status_code)
