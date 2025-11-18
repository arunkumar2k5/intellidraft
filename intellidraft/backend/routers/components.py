"""
API Routes for Component Processing
Handles all endpoints for single component and batch processing
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Dict, List, Optional
import shutil
from pathlib import Path

from services.openai_service import classify_component, get_component_description
from services.digikey_service import fetch_component_parameters
from services.document_service import update_functional_description, validate_template
from config import settings

router = APIRouter()

# Pydantic models for request/response
class ClassifyRequest(BaseModel):
    part_number: str

class ClassifyResponse(BaseModel):
    component_type: str
    confidence: str
    part_number: str

class FetchParametersRequest(BaseModel):
    part_number: str
    component_type: str

class GenerateDocumentRequest(BaseModel):
    template_path: str
    part_number: str
    component_type: str
    parameters: Dict[str, str]
    description: Optional[str] = ""

# Store uploaded template path temporarily (in production, use database or session)
uploaded_templates = {}

@router.post("/upload-template")
async def upload_template(file: UploadFile = File(...)):
    """
    Upload a template .docx file
    """
    try:
        # Validate file extension
        if not file.filename.endswith('.docx'):
            raise HTTPException(status_code=400, detail="Only .docx files are supported")
        
        # Save uploaded file
        file_path = settings.upload_dir / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Validate template
        validation = await validate_template(str(file_path))
        
        if not validation.get("valid"):
            # Remove invalid file
            file_path.unlink()
            raise HTTPException(status_code=400, detail=validation.get("error"))
        
        # Store template path (use session ID in production)
        template_id = file.filename
        uploaded_templates[template_id] = str(file_path)
        
        return {
            "success": True,
            "template_id": template_id,
            "filename": file.filename,
            "message": "Template uploaded successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@router.post("/classify-component", response_model=ClassifyResponse)
async def classify_component_endpoint(request: ClassifyRequest):
    """
    Classify component type using OpenAI
    """
    try:
        result = await classify_component(request.part_number)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Classification failed: {str(e)}")

@router.post("/fetch-parameters")
async def fetch_parameters_endpoint(request: FetchParametersRequest):
    """
    Fetch component parameters from Digi-Key API
    """
    try:
        result = await fetch_component_parameters(
            request.part_number,
            request.component_type
        )
        
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Parameter fetch failed: {str(e)}")

@router.post("/generate-document")
async def generate_document_endpoint(request: GenerateDocumentRequest):
    """
    Generate final document with parameters table in Functional Description section
    """
    try:
        # Resolve template path from template_id
        template_path = request.template_path
        
        # Check if it's a template_id (filename) rather than full path
        if template_path in uploaded_templates:
            template_path = uploaded_templates[template_path]
        
        # Verify template exists
        if not Path(template_path).exists():
            raise HTTPException(status_code=404, detail="Template file not found. Please upload a template first.")
        
        # Generate document
        result = await update_functional_description(
            template_path=template_path,
            part_number=request.part_number,
            parameters=request.parameters,
            component_type=request.component_type,
            description=request.description
        )
        
        if not result.get("success"):
            raise HTTPException(status_code=500, detail=result.get("error"))
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Document generation failed: {str(e)}")

@router.get("/download/{filename}")
async def download_document(filename: str):
    """
    Download generated document
    """
    file_path = settings.output_dir / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=str(file_path),
        filename=filename,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

@router.get("/templates")
async def list_templates():
    """
    List uploaded templates
    """
    return {
        "templates": [
            {"id": tid, "path": path}
            for tid, path in uploaded_templates.items()
        ]
    }
