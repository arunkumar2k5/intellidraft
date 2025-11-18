from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import sys
import csv
import json
import logging
from pathlib import Path
import threading

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from digikey import digikey_search
from gen_ai import genAi

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = os.path.join(os.path.expanduser("~"), "WCCA_Uploads")
MAX_FILE_SIZE = 25 * 1024 * 1024  # 25 MB
ALLOWED_EXTENSIONS = {
    'xml': ['.xml'],
    'csv': ['.csv'],
    'yaml': ['.yml', '.yaml']
}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Configure logging
logging.basicConfig(
    filename="uploader.log",
    level=logging.ERROR,
    format="%(asctime)s %(levelname)s:%(message)s"
)

# Global state for progress tracking
progress_state = {
    'total': 0,
    'done': 0,
    'status': 'idle'  # idle, processing, completed, error
}

def allowed_file(filename, file_type):
    """Check if file extension is allowed for the given type"""
    ext = os.path.splitext(filename)[1].lower()
    return ext in ALLOWED_EXTENSIONS.get(file_type, [])

def extract_part_numbers_from_csv(filepath):
    """Extract part numbers and IC chips from CSV file"""
    part_numbers = []
    ref_designators = []
    
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore", newline="") as f:
            sample = f.read(2048)
            f.seek(0)
            
            # Detect delimiter
            try:
                dialect = csv.Sniffer().sniff(sample, delimiters=[",", ";", "\t", "|"])
            except csv.Error:
                dialect = csv.get_dialect("excel")
            
            # Detect header
            has_header = False
            try:
                has_header = csv.Sniffer().has_header(sample)
            except Exception:
                has_header = False
            
            reader = csv.reader(f, dialect)
            for idx, row in enumerate(reader):
                if not row:
                    continue
                if has_header and idx == 0:
                    continue
                
                if len(row) >= 2:
                    part_number = row[0].strip()
                    ref_designator = row[1].strip()
                    if part_number:
                        part_numbers.append(part_number)
                        ref_designators.append(ref_designator)
        
        # Extract IC chips (components with 'U' in reference designator)
        chip_indices = [
            i for i, ref in enumerate(ref_designators)
            if "u" in ref.lower()
        ]
        chips = [part_numbers[i] for i in chip_indices]
        
        # De-duplicate while preserving order
        seen = set()
        unique_parts = [x for x in part_numbers if not (x in seen or seen.add(x))]
        
        return unique_parts, chips
        
    except Exception as e:
        logging.error(f"Error extracting part numbers from CSV: {e}", exc_info=True)
        raise

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok'})

@app.route('/api/upload/<file_type>', methods=['POST'])
def upload_file(file_type):
    """Upload and process file"""
    if file_type not in ALLOWED_EXTENSIONS:
        return jsonify({'error': 'Invalid file type'}), 400
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename, file_type):
        return jsonify({'error': f'Invalid file extension for {file_type}'}), 400
    
    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Handle duplicate filenames
        base, ext = os.path.splitext(filename)
        counter = 1
        while os.path.exists(filepath):
            filename = f"{base}({counter}){ext}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            counter += 1
        
        file.save(filepath)
        
        # Read file preview (first 10 lines)
        preview = []
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for i in range(10):
                line = f.readline()
                if not line:
                    break
                preview.append(line.rstrip())
        
        response = {
            'filename': filename,
            'filepath': filepath,
            'preview': preview
        }
        
        # If CSV, extract part numbers and trigger DigiKey search
        if file_type == 'csv':
            part_numbers, chips = extract_part_numbers_from_csv(filepath)
            response['part_numbers'] = part_numbers
            response['chips'] = chips
            response['total_parts'] = len(part_numbers)
            
            # Start DigiKey search in background
            def search_task():
                global progress_state
                progress_state['total'] = len(part_numbers)
                progress_state['done'] = 0
                progress_state['status'] = 'processing'
                
                def on_progress(done, total):
                    progress_state['done'] = done
                    progress_state['total'] = total
                
                try:
                    digikey_search(part_numbers, on_progress=on_progress)
                    progress_state['status'] = 'completed'
                except Exception as e:
                    logging.error(f"DigiKey search error: {e}", exc_info=True)
                    progress_state['status'] = 'error'
            
            threading.Thread(target=search_task, daemon=True).start()
        
        return jsonify(response), 200
        
    except Exception as e:
        logging.error(f"Upload error: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/api/progress', methods=['GET'])
def get_progress():
    """Get DigiKey search progress"""
    return jsonify(progress_state)

@app.route('/api/parts', methods=['GET'])
def get_parts():
    """Get parts data from parts.json"""
    try:
        parts_path = Path(__file__).parent.parent / "parts.json"
        if not parts_path.exists():
            return jsonify({'error': 'Parts data not available yet'}), 404
        
        with open(parts_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Categorize parts
        caps = [d for d in data if "Capacitance" in d]
        ress = [d for d in data if "Resistance" in d]
        others = [d for d in data if "Capacitance" not in d and "Resistance" not in d]
        
        return jsonify({
            'capacitors': caps,
            'resistors': ress,
            'others': others,
            'total': len(data)
        })
        
    except Exception as e:
        logging.error(f"Error reading parts: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/api/circuit-name', methods=['POST'])
def get_circuit_name():
    """Generate circuit name using GenAI"""
    try:
        data = request.get_json()
        chips = data.get('chips', [])
        
        if not chips:
            return jsonify({'circuit_name': 'Unknown Circuit'}), 200
        
        circuit_name = genAi(chips)
        return jsonify({'circuit_name': circuit_name})
        
    except Exception as e:
        logging.error(f"GenAI error: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/api/files/<filename>', methods=['GET'])
def get_file(filename):
    """Serve uploaded files"""
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except Exception as e:
        return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
