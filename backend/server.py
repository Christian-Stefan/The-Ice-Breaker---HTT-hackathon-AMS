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

### Hard Coded Stuff Start ### 
# -- CONFIG
GREENPT_API_KEY = "sk-CpkdZT1zSlekZOrSv8htAdFeYeiAPkIlqlBuvoyX-vQ"
GREENPT_BASE_URL = "https://api.greenpt.ai/v1"
MODEL_ID = "green-l-raw" 
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

# Routes
@api_router.get("/")
async def root():
    return {"message": "Clothing Sustainability Scanner API"}

@api_router.post("/analyze-clothing")
async def analyze_clothing(request: AnalyzeClothingRequest):
    print("Request received!")
    print(request)

    data = request.model_dump()
    image_64 = data.get("image_base64")
    clothing_type = data.get("clothing_type")

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
        print(json.loads(raw_content))
        return json.loads(raw_content)
    except json.JSONDecodeError:
        print("❌ Failed to parse JSON. Model output was not valid JSON.")
        return {"error": "Parsing failed", "raw_output": raw_content}

    """
    try:
        logger.info(f"Starting analysis for {request.scan_type}")
        
        # Get API key from environment
        api_key = os.getenv("EMERGENT_LLM_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="API key not configured")
        
        # Create LLM chat instance
        session_id = f"clothing-scan-{uuid.uuid4()}"
        chat = LlmChat(
            api_key=api_key,
            session_id=session_id,
            system_message="You are an expert in textile analysis, fashion sustainability, and environmental impact assessment. Provide detailed, accurate information about clothing materials, longevity, and recyclability."
        )
        
        # Use GPT-4o model
        chat.with_model("openai", "gpt-4o")
        
        # Create the analysis prompt based on scan type
        if request.scan_type == "label":
            prompt = ""Analyze this clothing label image and provide a detailed sustainability assessment in the following JSON format:

{
  "materials": [list of materials/fabrics identified],
  "longevity": "Expected lifespan and durability assessment (e.g., '5-10 years with proper care')",
  "recyclability": "Detailed recyclability information including how and where to recycle",
  "care_instructions": "Detailed care instructions to maximize garment lifespan",
  "environmental_impact": "Assessment of environmental impact including water usage, chemical processing, carbon footprint",
  "sustainability_score": "Overall score from 1-10 with brief explanation"
}

Provide only the JSON response, no additional text.""
        else:
            prompt = ""Analyze this clothing/garment image and provide a detailed sustainability assessment in the following JSON format:

{
  "materials": [list of likely materials/fabrics based on visual appearance],
  "longevity": "Expected lifespan and durability assessment based on construction and material",
  "recyclability": "General recyclability information for this type of garment",
  "care_instructions": "Recommended care instructions for this type of garment",
  "environmental_impact": "Assessment of typical environmental impact for this type of garment",
  "sustainability_score": "Overall estimated score from 1-10 with brief explanation"
}

Provide only the JSON response, no additional text.""
        
        # Create image content from base64
        image_content = ImageContent(image_base64=request.image_base64)
        
        # Create user message with image
        user_message = UserMessage(
            text=prompt,
            file_contents=[image_content]
        )
        
        # Get response from AI
        logger.info("Sending request to OpenAI Vision API")
        response = await chat.send_message(user_message)
        logger.info(f"Received response: {response[:200]}...")
        
        # Parse the JSON response
        import json
        # Remove markdown code blocks if present
        clean_response = response.strip()
        if clean_response.startswith("```json"):
            clean_response = clean_response[7:]
        if clean_response.startswith("```"):
            clean_response = clean_response[3:]
        if clean_response.endswith("```"):
            clean_response = clean_response[:-3]
        clean_response = clean_response.strip()
        
        analysis_data = json.loads(clean_response)
        
        # Create analysis object
        analysis = ClothingAnalysis(**analysis_data)
        
        # Save to database
        scan_result = ScanResult(
            image_base64=request.image_base64,
            analysis=analysis,
            scan_type=request.scan_type
        )
        
        await db.scans.insert_one(scan_result.dict())
        logger.info(f"Saved scan result with ID: {scan_result.id}")
        
        return {
            "success": True,
            "scan_id": scan_result.id,
            "analysis": analysis.dict()
        }
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error: {e}")
        logger.error(f"Response was: {response}")
        raise HTTPException(status_code=500, detail=f"Failed to parse AI response: {str(e)}")
    except Exception as e:
        logger.error(f"Error analyzing clothing: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    """

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