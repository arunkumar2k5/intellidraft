"""
OpenRouter Service - Component Classification
Uses OpenRouter API to classify electronic component types from part numbers
OpenRouter provides access to multiple LLM models through a unified API
"""
import requests
from typing import Optional
from config import settings

# OpenRouter API configuration
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_API_KEY = settings.openrouter_api_key

async def classify_component(part_number: str) -> dict:
    """
    Classify the component type using OpenAI API
    
    Args:
        part_number: Electronic component part number
        
    Returns:
        dict with 'component_type' and 'confidence'
    """
    try:
        prompt = f"""You are an expert in electronic components. Given the part number below, identify the component type.

Part Number: {part_number}

Respond with ONLY ONE of these exact component types (lowercase):
- resistor
- capacitor
- inductor
- diode
- transistor
- ic (integrated circuit)
- connector
- other

If you're unsure, respond with 'other'.

Component type:"""

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:3000",  # Optional, for rankings
            "X-Title": "IntelliDraft"  # Optional, for rankings
        }
        
        payload = {
            "model": "openai/gpt-3.5-turbo",  # Can use other models like "anthropic/claude-3-haiku"
            "messages": [
                {"role": "system", "content": "You are an expert in electronic component identification. Respond with only the component type in lowercase."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 20
        }
        
        response = requests.post(OPENROUTER_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        component_type = result['choices'][0]['message']['content'].strip().lower()
        
        # Validate response
        valid_types = ["resistor", "capacitor", "inductor", "diode", "transistor", "ic", "connector", "other"]
        if component_type not in valid_types:
            component_type = "other"
        
        return {
            "component_type": component_type,
            "confidence": "high",
            "part_number": part_number
        }
        
    except Exception as e:
        print(f"OpenRouter classification error: {e}")
        return {
            "component_type": "other",
            "confidence": "low",
            "error": str(e),
            "part_number": part_number
        }

async def get_component_description(component_type: str, parameters: dict) -> str:
    """
    Generate a natural language description of the component based on its parameters
    
    Args:
        component_type: Type of component
        parameters: Dictionary of component parameters
        
    Returns:
        Natural language description
    """
    try:
        params_text = "\n".join([f"- {k}: {v}" for k, v in parameters.items()])
        
        prompt = f"""Generate a concise technical description (2-3 sentences) for this {component_type}:

Parameters:
{params_text}

Description:"""

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:3000",
            "X-Title": "IntelliDraft"
        }
        
        payload = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are a technical writer specializing in electronic component documentation."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.5,
            "max_tokens": 150
        }
        
        response = requests.post(OPENROUTER_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        return result['choices'][0]['message']['content'].strip()
        
    except Exception as e:
        print(f"Description generation error: {e}")
        return f"A {component_type} component with the specified parameters."
