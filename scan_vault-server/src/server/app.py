from fastapi import FastAPI, logger
from fastapi.middleware.cors import CORSMiddleware
import logging, sys
from src.utils.utils import read_markdown_file
from src.server.routes.scan import router as scan_router

readme_content = read_markdown_file("README.md")

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Scan Vault",
    description=(lambda: readme_content if isinstance(readme_content, str) else "")(),
    version="1.0.0",
)

@app.on_event("startup")
async def sync_database():
    logger.debug("starting up...")


app.include_router(scan_router, tags=["Scan"]) 


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


