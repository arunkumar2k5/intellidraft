import pandas as pd
import json
import sys

def excel_to_json(excel_file_path, json_file_path=None):
    """
    Convert Excel file with five columns to JSON format.
    
    Args:
        excel_file_path: Path to the input Excel file
        json_file_path: Path to the output JSON file (optional)
    """
    try:
        # Read Excel file
        df = pd.read_excel(excel_file_path)
        
        # Convert DataFrame to list of dictionaries
        parameters_list = []
        for _, row in df.iterrows():
            param = {
                "name": row.get('name', ''),
                "value": row.get('Value', ''),
                "unit": row.get('Unit', ''),
                "Symbol": row.get('Symbol', None),
                "confidence": int(row.get('Confidence', 0)) if pd.notna(row.get('Confidence', 0)) else 0
            }
            parameters_list.append(param)
        
        # Create final structure
        result = {"parameters": parameters_list}
        
        # If no output path specified, create one based on input file
        if json_file_path is None:
            json_file_path = excel_file_path.rsplit('.', 1)[0] + '.json'
        
        # Write to JSON file
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(result, json_file, indent=2, ensure_ascii=False)
        
        print(f"Successfully converted '{excel_file_path}' to '{json_file_path}'")
        print(f"Total parameters: {len(parameters_list)}")
        
        return json_file_path
        
    except FileNotFoundError:
        print(f"Error: File '{excel_file_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    # Example usage
    if len(sys.argv) > 1:
        # Use command line argument
        excel_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
    else:
        # Default file path - modify this to your Excel file location
        excel_file = "LDO.xlsx"  # Change this to your Excel file path
        output_file = "LDO_parameters.json"  # Change this to your desired output path
    
    excel_to_json(excel_file, output_file)