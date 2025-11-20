from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime
# from emergentintegrations.llm.chat import LlmChat, UserMessage, ImageContent
import base64
import json 
from openai import OpenAI
from matplotlib import pyplot as plt 
from firecrawl import Firecrawl
from fastapi.responses import JSONResponse

### Hard Coded Stuff Start ### 
# -- CONFIG
GREENPT_API_KEY = "sk-CpkdZT1zSlekZOrSv8htAdFeYeiAPkIlqlBuvoyX-vQ"
GREENPT_BASE_URL = "https://api.greenpt.ai/v1"
MODEL_ID = "green-l-raw" 

FIRECRAWL_API_KEY = "fc-d129a30298c54d64a4043dbfc85ee899"
# -- CONFIG
### Hard Coded Stuff End ###

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Models
class AnalyzeClothingRequest(BaseModel):
    image_base64: str
    scan_type: str  # "label" or "garment"

class ClothingAnalysis(BaseModel):
    materials: List[str]
    longevity: str
    recyclability: str
    care_instructions: str
    environmental_impact: str
    sustainability_score: Optional[str] = None

class ScanResult(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    image_base64: str
    analysis: ClothingAnalysis
    scan_type: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ScanResultResponse(BaseModel):
    id: str
    image_base64: str
    analysis: ClothingAnalysis
    scan_type: str
    timestamp: str

class AnalyzeClothingRequest(BaseModel):
    image_base64: str
    scan_type: str
    clothing_type: str

class ClothingRequest(BaseModel):
    clothing_type: str

# Routes
@api_router.get("/")
async def root():
    return {"message": "Clothing Sustainability Scanner API"}

@api_router.post("/search-alternatives")
async def search_alternatives(request: ClothingRequest):
    print("Request received!")
    print("Scanning alternatives")
    print(request.clothing_type)

    clothing_item = request.clothing_type
    firecrawl = Firecrawl(api_key=FIRECRAWL_API_KEY)

    query = f"environmentally friendly {clothing_item} Amsterdam"

    results = firecrawl.search(
        query=query,
        limit=5,
    )

    web_queries = results.web

    print(web_queries)

    web_serializable = [
        {
            "url": w.url,
            "title": w.title,
            "description": w.description
        }
        for w in web_queries
    ]

    print()
    print("Formatted")
    print(web_serializable)
    return JSONResponse(content={"web": web_serializable})

@api_router.post("/analyze-clothing")
async def analyze_clothing(request: AnalyzeClothingRequest):
    print("Request received!")
    #data = request.model_dump()
    #image_64 = data.get("image_base64")
    #clothing_type = data.get("clothing_type")

    image_64 = request.image_base64
    clothing_type = request.clothing_type

    print("Clothing type:")
    print(clothing_type)

    try:
        print(f"Connecting to GreenPT at {GREENPT_BASE_URL}...")
        client = OpenAI(
            api_key=GREENPT_API_KEY,
            base_url=GREENPT_BASE_URL
        )
        print("Connection successful!")        
    except Exception as e:
        print(f"\n❌ Error: {e}")

    print("🧥 Analyzing label with GreenPT...")
    # We define the strict JSON structure we want the AI to mimic
    json_structure_example = """
    {
        "carbon_footprint" : "10 CO2e",
        "material_composition" : [
            {"material_name" : "acrylic", "environmental_consequence" : "Microplastic Pollution: ..."}, 
            {"material_name" : "polyester", "environmental_consequence" : "Non-Biodegradable: ..."}
        ],
        "country_origin" : "China",
        "expected_durability" : "5 years",
        "final_decision" : false,
        "sustainable_tips": ["Tip 1", "Tip 2", "Tip 3"]
    }
    """

    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful expert in sustainable fashion practices. You have profound knowledge of the fast fashion industry. You will be providing advice to consumers on their clothing purchases. OUTPUT RAW JSON ONLY. NO MARKDOWN."
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text", 
                        "text": f"""
                        Consider the label in the image provided. It belongs to a {clothing_type}. 
                        From all available information determine the following metrics for the item of clothing to which this label belongs: 
                        carbon footprint (in CO2 equivalents), material composition, country of origin, durability.

                        Format the output as a JSON object exactly like this example:
                        {json_structure_example}

                        For each harmful material, explain the environmental consequences in at most 50 words. 
                        Based on your analysis of the previous metrics give a final boolean (true/false) decision on whether the clothing is environmentally sustainable.
                        Finally, populate the 'sustainable_tips' list with 3 suggestions on how the user can make more sustainable decisions for their existing item of clothing.
                        """
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"{image_64}"
                        },
                    },
                ],
            }
        ],
        temperature=0.1,
    )

    # --- PARSING LOGIC ---
    raw_content = response.choices[0].message.content
    
    # Clean up Markdown if the model adds ```json ... ```
    if "```json" in raw_content:
        raw_content = raw_content.split("```json")[1].split("```")[0]
    elif "```" in raw_content:
        raw_content = raw_content.split("```")[1].split("```")[0]
        
    try:
        print("Clothing type final: ")
        print(clothing_type)
        final_data = json.loads(raw_content)
        final_data["clothing_type"] = clothing_type
        print(final_data)

        return final_data
    except json.JSONDecodeError:
        print("❌ Failed to parse JSON. Model output was not valid JSON.")
        return {"error": "Parsing failed", "raw_output": raw_content}

@api_router.get("/scan-history", response_model=List[ScanResultResponse])
async def get_scan_history():
    try:
        scans = await db.scans.find().sort("timestamp", -1).to_list(100)
        
        # Convert to response model
        results = []
        for scan in scans:
            results.append(ScanResultResponse(
                id=scan["id"],
                image_base64=scan["image_base64"],
                analysis=ClothingAnalysis(**scan["analysis"]),
                scan_type=scan["scan_type"],
                timestamp=scan["timestamp"].isoformat()
            ))
        
        return results
    except Exception as e:
        logger.error(f"Error fetching scan history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.delete("/scan/{scan_id}")
async def delete_scan(scan_id: str):
    try:
        result = await db.scans.delete_one({"id": scan_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Scan not found")
        return {"success": True, "message": "Scan deleted"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting scan: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()