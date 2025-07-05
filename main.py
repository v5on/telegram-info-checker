from fastapi import FastAPI, Query
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI()

# Allow all CORS (adjust in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPSTREAM_BASE_URL = "https://tele-user-info-api-production.up.railway.app"

@app.get("/check")
async def check_phones(phones: str = Query(...)):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{UPSTREAM_BASE_URL}/check", params={"phones": phones})
            data = response.json()

            valid = []
            invalid = []

            for user in data.get("results", []):
                phone = user.get("phone", "")
                username = user.get("username")
                first_name = user.get("first_name")
                last_name = user.get("last_name") or ""

                if username:
                    name = f"@{username}"
                    valid.append(f"✅ {phone} → {name}")
                elif first_name:
                    name = f"{first_name} {last_name}".strip()
                    valid.append(f"✅ {phone} → {name}")
                else:
                    invalid.append(f"❌ {phone} → No Telegram account found")

            output = ""
            if valid:
                output += "✅ Valid Accounts:\n" + "\n".join(valid) + "\n\n"
            if invalid:
                output += "❌ Invalid Accounts:\n" + "\n".join(invalid)

            return PlainTextResponse(content=output.strip(), status_code=200)

        except Exception as e:
            return PlainTextResponse(content=f"❌ Error: {str(e)}", status_code=500)


@app.get("/get_user_info")
async def get_user_info(username: str = Query(...)):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{UPSTREAM_BASE_URL}/get_user_info", params={"username": username})
            return PlainTextResponse(content=response.text, status_code=response.status_code)
        except Exception as e:
            return PlainTextResponse(content=f"❌ Error: {str(e)}", status_code=500)
