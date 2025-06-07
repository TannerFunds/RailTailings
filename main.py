"""
Railway-optimized TailingsIQ API Gateway
Simplified version for easy deployment
"""
import os
import time
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import motor.motor_asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="TailingsIQ API",
    description="Railway-optimized API for TailingsIQ tailings management system",
    version="1.0.0"
)

# Add CORS middleware - Railway handles HTTPS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OAuth2 password bearer for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Database connection
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URI)
database = client.tailingsiq

# Pydantic models
class FacilityCreate(BaseModel):
    name: str
    location: str
    type: str
    owner: str
    status: str = "active"

class FacilityResponse(BaseModel):
    id: str
    name: str
    location: str
    type: str
    owner: str
    status: str
    created_at: str

class DocumentCreate(BaseModel):
    name: str
    type: str
    facility_id: str
    content: str

class DocumentResponse(BaseModel):
    id: str
    name: str
    type: str
    facility_id: str
    created_at: str

class MonitoringData(BaseModel):
    facility_id: str
    timestamp: float
    readings: Dict[str, Any]

class RiskAssessment(BaseModel):
    facility_id: str
    risk_level: str
    risk_score: int
    factors: List[str]
    recommendations: List[str]

# Dependency for authentication (simplified for Railway)
async def get_current_user(token: str = Depends(oauth2_scheme)):
    # Simplified authentication - implement proper JWT validation in production
    return {"username": "demo_user", "role": "admin"}

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for Railway monitoring"""
    return {
        "status": "healthy", 
        "timestamp": time.time(),
        "service": "tailingsiq-api"
    }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "TailingsIQ API - Railway Deployment",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

# Authentication endpoints
@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Simplified login endpoint"""
    # In production, implement proper authentication
    if form_data.username == "demo" and form_data.password == "demo":
        return {
            "access_token": "demo_token_12345",
            "token_type": "bearer"
        }
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password"
    )

# Facility management endpoints
@app.post("/facilities", response_model=FacilityResponse)
async def create_facility(
    facility: FacilityCreate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Create a new facility"""
    try:
        facility_doc = {
            **facility.dict(),
            "created_at": time.time(),
            "updated_at": time.time()
        }
        result = await database.facilities.insert_one(facility_doc)
        facility_doc["id"] = str(result.inserted_id)
        facility_doc["created_at"] = str(facility_doc["created_at"])
        return FacilityResponse(**facility_doc)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/facilities")
async def list_facilities(
    owner: Optional[str] = None,
    status: Optional[str] = None,
    type: Optional[str] = None,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """List all facilities with optional filters"""
    try:
        query = {}
        if owner:
            query["owner"] = owner
        if status:
            query["status"] = status
        if type:
            query["type"] = type
        
        cursor = database.facilities.find(query)
        facilities = []
        async for facility in cursor:
            facility["id"] = str(facility["_id"])
            del facility["_id"]
            facilities.append(facility)
        
        return facilities
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/facilities/{facility_id}")
async def get_facility(
    facility_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get a specific facility by ID"""
    try:
        from bson import ObjectId
        facility = await database.facilities.find_one({"_id": ObjectId(facility_id)})
        if not facility:
            raise HTTPException(status_code=404, detail="Facility not found")
        
        facility["id"] = str(facility["_id"])
        del facility["_id"]
        return facility
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Document management endpoints
@app.post("/documents", response_model=DocumentResponse)
async def upload_document(
    document: DocumentCreate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Upload a new document"""
    try:
        document_doc = {
            **document.dict(),
            "created_at": time.time(),
            "updated_at": time.time()
        }
        result = await database.documents.insert_one(document_doc)
        document_doc["id"] = str(result.inserted_id)
        document_doc["created_at"] = str(document_doc["created_at"])
        return DocumentResponse(**document_doc)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/documents/{document_id}")
async def get_document(
    document_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get a specific document by ID"""
    try:
        from bson import ObjectId
        document = await database.documents.find_one({"_id": ObjectId(document_id)})
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        
        document["id"] = str(document["_id"])
        del document["_id"]
        return document
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Monitoring endpoints
@app.get("/facilities/{facility_id}/monitoring")
async def get_monitoring_data(
    facility_id: str,
    start_time: Optional[float] = None,
    end_time: Optional[float] = None,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get monitoring data for a facility"""
    try:
        if not start_time:
            start_time = time.time() - (7 * 24 * 60 * 60)  # 7 days ago
        if not end_time:
            end_time = time.time()
        
        query = {
            "facility_id": facility_id,
            "timestamp": {"$gte": start_time, "$lte": end_time}
        }
        
        cursor = database.monitoring.find(query)
        readings = []
        async for reading in cursor:
            reading["id"] = str(reading["_id"])
            del reading["_id"]
            readings.append(reading)
        
        return {
            "facility_id": facility_id,
            "start_time": start_time,
            "end_time": end_time,
            "readings": readings
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/facilities/{facility_id}/monitoring")
async def add_monitoring_data(
    facility_id: str,
    data: MonitoringData,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Add new monitoring data for a facility"""
    try:
        monitoring_doc = {
            "facility_id": facility_id,
            "timestamp": data.timestamp,
            "readings": data.readings,
            "created_at": time.time()
        }
        result = await database.monitoring.insert_one(monitoring_doc)
        monitoring_doc["id"] = str(result.inserted_id)
        return monitoring_doc
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Risk assessment endpoints
@app.post("/facilities/{facility_id}/risk-assessment")
async def assess_facility_risk(
    facility_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Perform risk assessment for a facility"""
    try:
        # Simplified risk assessment - integrate with AI models in production
        assessment = {
            "facility_id": facility_id,
            "assessment_id": f"assessment_{int(time.time())}",
            "timestamp": time.time(),
            "overall_risk_level": "medium",
            "risk_score": 65,
            "summary": "Automated risk assessment completed",
            "risk_factors": [
                {"category": "structural", "severity": "medium", "description": "Foundation stability"},
                {"category": "environmental", "severity": "low", "description": "Water quality impact"}
            ],
            "recommendations": [
                "Increase monitoring frequency",
                "Schedule structural inspection",
                "Review environmental controls"
            ]
        }
        
        # Store assessment in database
        result = await database.assessments.insert_one(assessment)
        assessment["id"] = str(result.inserted_id)
        
        return assessment
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/facilities/{facility_id}/risk-factors")
async def get_risk_factors(
    facility_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get risk factors for a facility"""
    try:
        # Simplified risk factors - integrate with AI analysis in production
        risk_factors = [
            {
                "id": f"risk_factor_1_{facility_id}",
                "category": "structural",
                "description": "Foundation settlement detected",
                "severity": "medium",
                "probability": 0.3,
                "impact": 0.7
            },
            {
                "id": f"risk_factor_2_{facility_id}",
                "category": "environmental",
                "description": "Groundwater contamination risk",
                "severity": "low",
                "probability": 0.2,
                "impact": 0.5
            }
        ]
        return risk_factors
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# AI inference endpoints (simplified)
@app.post("/inference/query")
async def query_model(
    query: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Query AI model for analysis"""
    try:
        # Simplified AI response - integrate with OpenAI/Anthropic in production
        response = {
            "query": query.get("text", ""),
            "response": "This is a simplified AI response. Integrate with OpenAI/Anthropic APIs for production use.",
            "model": "simplified_model",
            "timestamp": time.time(),
            "usage": {
                "prompt_tokens": 10,
                "completion_tokens": 20,
                "total_tokens": 30
            }
        }
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Railway-specific configuration
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False  # Disable reload in production
    )

