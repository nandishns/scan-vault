from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def home():
    return {"message": "Scan Vault API is up and running"} 
