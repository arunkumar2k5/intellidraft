"""
Digi-Key Service - Parameter Extraction
Wrapper around the existing digikey.py module to fetch component parameters
"""
import sys
import json
from pathlib import Path
from typing import List, Dict, Optional

# Add Library folder to path
library_path = Path(__file__).parent.parent.parent / "Library"
sys.path.insert(0, str(library_path))

from digikey import digikey_search

# Load parameters configuration
PARAMS_CONFIG_PATH = library_path / "parameters.json"

def load_parameters_config() -> dict:
    """Load the parameters.json configuration file"""
    with open(PARAMS_CONFIG_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_required_parameters(component_type: str) -> List[str]:
    """
    Get the list of required parameters for a component type
    
    Args:
        component_type: Type of component (resistor, capacitor, etc.)
        
    Returns:
        List of parameter names to extract
    """
    config = load_parameters_config()
    if component_type in config:
        return config[component_type].get("key_parameters", [])
    return []

async def fetch_component_parameters(part_number: str, component_type: str) -> dict:
    """
    Fetch component parameters from Digi-Key API
    
    Args:
        part_number: Component part number
        component_type: Type of component
        
    Returns:
        Dictionary with filtered parameters based on component type
    """
    try:
        # Get required parameters for this component type
        required_params = get_required_parameters(component_type)
        
        # Initialize with empty parameters from parameters.json
        filtered_params = {}
        for param in required_params:
            # Convert snake_case to Title Case for display
            display_name = param.replace("_", " ").title()
            filtered_params[display_name] = ""
        
        try:
            # Call the existing digikey_search function
            # It expects a list of part numbers
            result = digikey_search([part_number])
            
            # Read the generated parts.json file
            parts_json_path = library_path / "parts.json"
            
            if parts_json_path.exists():
                with open(parts_json_path, 'r', encoding='utf-8') as f:
                    parts_data = json.load(f)
                
                if parts_data and len(parts_data) > 0:
                    # Get the first result
                    raw_params = parts_data[0]
                    
                    # Always include basic info if available
                    if "Part Number" in raw_params:
                        filtered_params["Part Number"] = raw_params["Part Number"]
                    if "Mfr" in raw_params:
                        filtered_params["Manufacturer"] = raw_params["Mfr"]
                    if "Part Status" in raw_params:
                        filtered_params["Part Status"] = raw_params["Part Status"]
                    
                    # Map required parameters (case-insensitive matching)
                    for req_param in required_params:
                        # Try to find matching parameter in raw data
                        for key, value in raw_params.items():
                            # Normalize both strings for comparison
                            if req_param.lower().replace("_", " ") in key.lower().replace("-", " "):
                                filtered_params[key] = value
                                break
        except Exception as digikey_error:
            print(f"Digi-Key API error (will use empty template): {digikey_error}")
            # Continue with empty parameters - user can fill them manually
        
        return {
            "component_type": component_type,
            "parameters": filtered_params,
            "message": "Parameters loaded. Fill in values manually if Digi-Key data is unavailable."
        }
        
    except Exception as e:
        print(f"Parameter fetch error: {e}")
        # Return empty parameters as fallback
        required_params = get_required_parameters(component_type)
        filtered_params = {}
        for param in required_params:
            display_name = param.replace("_", " ").title()
            filtered_params[display_name] = ""
        
        return {
            "component_type": component_type,
            "parameters": filtered_params,
            "message": "Using parameter template. Please fill in values manually."
        }

def get_component_description(component_type: str) -> str:
    """Get the description for a component type"""
    config = load_parameters_config()
    if component_type in config:
        return config[component_type].get("description", "")
    return ""
