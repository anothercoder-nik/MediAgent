from flask import Flask, request, jsonify, send_file
import tempfile
import re
from werkzeug.utils import secure_filename
import os
import json
import tempfile
from datetime import datetime
from Utils.Agents import (
    extract_text_from_pdf, structure_medical_report,
    Cardiologist, Psychologist, Pulmonologist, MultidisciplinaryTeam,
    generate_report_pdf
)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Use a more Railway-friendly upload path
upload_folder = os.environ.get('UPLOAD_FOLDER', 'uploads')
app.config['UPLOAD_FOLDER'] = upload_folder

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Medical Diagnostics API"
    })

@app.route('/upload-pdf', methods=['POST'])
def upload_pdf():
    """
    Upload a PDF file
    Returns: JSON with file path and metadata
    """
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Check file type
        if not allowed_file(file.filename):
            return jsonify({"error": "Invalid file type. Only PDF files are allowed"}), 400
        
        # Secure filename and save
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        file.save(file_path)
        
        return jsonify({
            "message": "File uploaded successfully",
            "file_path": file_path,
            "filename": filename,
            "upload_time": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Upload failed: {str(e)}"}), 500

@app.route('/extract-text', methods=['POST'])
def extract_text():
    """
    Extract text from uploaded PDF
    Expects: JSON { "path": "<uploaded_pdf_path>" }
    Returns: JSON with extracted text
    """
    try:
        data = request.get_json()
        
        if not data or 'path' not in data:
            return jsonify({"error": "PDF path is required"}), 400
        
        pdf_path = data['path']
        
        # Check if file exists
        if not os.path.exists(pdf_path):
            return jsonify({"error": "PDF file not found"}), 404
        
        # Extract text
        extracted_text = extract_text_from_pdf(pdf_path)
        
        if not extracted_text:
            return jsonify({"error": "No text could be extracted from PDF"}), 400
        
        return jsonify({
            "message": "Text extracted successfully",
            "raw_text": extracted_text,
            "text_length": len(extracted_text),
            "extraction_time": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Text extraction failed: {str(e)}"}), 500

@app.route('/structure-report', methods=['POST'])
def structure_report():
    """
    Structure raw text into medical report format
    Expects: JSON { "text": "<raw_text>" }
    Returns: JSON with structured report
    """
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({"error": "Raw text is required"}), 400
        
        raw_text = data['text']
        
        if not raw_text.strip():
            return jsonify({"error": "Text cannot be empty"}), 400
        
        # Structure the report
        structured_report = structure_medical_report(raw_text)
        
        return jsonify({
            "message": "Report structured successfully",
            "structured_report": structured_report,
            "processing_time": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Report structuring failed: {str(e)}"}), 500

@app.route('/run-agent/<agent_type>', methods=['POST'])
def run_agent(agent_type):
    """
    Run specific AI agent on structured report
    Expects: JSON { "text": "<structured_text>" }
    Returns: JSON with agent assessment
    """
    try:
        # Validate agent type
        valid_agents = ['cardiologist', 'psychologist', 'pulmonologist']
        if agent_type.lower() not in valid_agents:
            return jsonify({"error": f"Invalid agent type. Must be one of: {valid_agents}"}), 400
        
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({"error": "Structured text is required"}), 400
        
        structured_text = data['text']
        
        if not structured_text.strip():
            return jsonify({"error": "Structured text cannot be empty"}), 400
        
        # Create and run the appropriate agent
        agent_class_map = {
            'cardiologist': Cardiologist,
            'psychologist': Psychologist,
            'pulmonologist': Pulmonologist
        }
        
        agent_class = agent_class_map[agent_type.lower()]
        agent = agent_class(structured_text)
        result = agent.run()
        
        if result is None:
            return jsonify({"error": f"{agent_type} agent failed to process the report"}), 500
        
        return jsonify({
            "message": f"{agent_type.title()} assessment completed",
            "agent_type": agent_type.lower(),
            "assessment": result,
            "processing_time": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"{agent_type} agent failed: {str(e)}"}), 500

from flask import make_response, jsonify

from flask import Flask, request, make_response
import json
from datetime import datetime

@app.route('/multidisciplinary-summary', methods=['POST'])
def multidisciplinary_summary():
    try:
        data = request.get_json()
        
        if not data:
            response = make_response(json.dumps({"error": "Request body is required"}), 400)
            response.headers['Content-Type'] = 'application/json; charset=utf-8'
            return response
        
        required_fields = ['cardiologist', 'psychologist', 'pulmonologist']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            response = make_response(json.dumps({"error": f"Missing required fields: {missing_fields}"}), 400)
            response.headers['Content-Type'] = 'application/json; charset=utf-8'
            return response
        
        for field in required_fields:
            if not data[field] or not data[field].strip():
                response = make_response(json.dumps({"error": f"{field} assessment cannot be empty"}), 400)
                response.headers['Content-Type'] = 'application/json; charset=utf-8'
                return response
        
        team = MultidisciplinaryTeam(
            data['cardiologist'],
            data['psychologist'], 
            data['pulmonologist']
        )
        
        summary = team.run()
        
        if not summary:
            response = make_response(json.dumps({"error": "Failed to generate multidisciplinary summary"}), 500)
            response.headers['Content-Type'] = 'application/json; charset=utf-8'
            return response
        
        response_data = {
            "message": "Multidisciplinary summary generated successfully",
            "summary": summary,
            "processing_time": datetime.now().isoformat()
        }
        response = make_response(json.dumps(response_data), 200)
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response
        
    except Exception as e:
        response = make_response(json.dumps({"error": f"Multidisciplinary summary failed: {str(e)}"}), 500)
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response


@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    """
    Generate final PDF report
    Expects: JSON Array with a single object { 
        "structured_report": "<structured_text>", 
        "cardiologist": "<assessment>", 
        "psychologist": "<assessment>", 
        "pulmonologist": "<assessment>", 
        "final_summary": "<summary>"
    }
    Returns: Downloadable PDF file
    """
    try:
        data = request.get_json()

        # Handle case when n8n sends array of items
        if isinstance(data, list) and len(data) == 1:
            data = data[0]

        if not isinstance(data, dict):
            return jsonify({"error": "Invalid data format. Expected JSON object."}), 400

        required_fields = [
            'structured_report', 'cardiologist', 'psychologist',
            'pulmonologist', 'final_summary'
        ]
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            return jsonify({"error": f"Missing required fields: {missing_fields}"}), 400

        # Validate that all fields have content
        for field in required_fields:
            if not data[field] or not data[field].strip():
                return jsonify({"error": f"{field} cannot be empty"}), 400

        # Create temporary PDF file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_filename = f"medical_report_{timestamp}.pdf"
        pdf_path = os.path.join(tempfile.gettempdir(), pdf_filename)

        # Prepare agent responses dictionary
        agent_responses = {
            'Cardiologist': data['cardiologist'],
            'Psychologist': data['psychologist'],
            'Pulmonologist': data['pulmonologist']
        }

        print("Structured Report Preview:", data['structured_report'][:100])
        print("Cardiologist Report Preview:", data['cardiologist'][:100])

        # Generate PDF
        generate_report_pdf(
            pdf_path,
            data['structured_report'],
            agent_responses,
            data['final_summary']
        )

        # Check if PDF was created successfully
        if not os.path.exists(pdf_path):
            return jsonify({"error": "PDF generation failed"}), 500

        # Return PDF file for download
        return send_file(
            pdf_path,
            as_attachment=True,
            download_name=pdf_filename,
            mimetype='application/pdf'
        )

    except Exception as e:
        return jsonify({"error": f"PDF generation failed: {str(e)}"}), 500



@app.route('/process-complete', methods=['POST'])
def process_complete():
    """
    Complete end-to-end processing (convenience endpoint)
    Expects: JSON { "pdf_path": "<path_to_uploaded_pdf>" }
    Returns: Downloadable PDF with complete analysis
    """
    try:
        data = request.get_json()
        
        if not data or 'pdf_path' not in data:
            return jsonify({"error": "PDF path is required"}), 400
        
        pdf_path = data['pdf_path']
        
        # Check if file exists
        if not os.path.exists(pdf_path):
            return jsonify({"error": "PDF file not found"}), 404
        
        # Step 1: Extract text
        raw_text = extract_text_from_pdf(pdf_path)
        
        # Step 2: Structure report
        structured_report = structure_medical_report(raw_text)
        
        # Step 3: Run all agents
        cardiologist = Cardiologist(structured_report)
        psychologist = Psychologist(structured_report)
        pulmonologist = Pulmonologist(structured_report)
        
        cardio_result = cardiologist.run()
        psycho_result = psychologist.run()
        pulmo_result = pulmonologist.run()
        
        # Step 4: Generate multidisciplinary summary
        team = MultidisciplinaryTeam(cardio_result, psycho_result, pulmo_result)
        final_summary = team.run()
        
        # Step 5: Generate PDF (without Hindi translation)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_filename = f"complete_medical_report_{timestamp}.pdf"
        output_pdf_path = os.path.join(tempfile.gettempdir(), pdf_filename)
        
        agent_responses = {
            'Cardiologist': cardio_result,
            'Psychologist': psycho_result,
            'Pulmonologist': pulmo_result
        }
        
        generate_report_pdf(
            output_pdf_path,
            structured_report,
            agent_responses,
            final_summary
        )
        
        # Return PDF file for download
        return send_file(
            output_pdf_path,
            as_attachment=True,
            download_name=pdf_filename,
            mimetype='application/pdf'
        )
        
    except Exception as e:
        return jsonify({"error": f"Complete processing failed: {str(e)}"}), 500

@app.errorhandler(413)
def too_large(e):
    return jsonify({"error": "File too large. Maximum size is 16MB"}), 413

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    # Get port from environment variable (Railway sets this automatically)
    port = int(os.environ.get('PORT', 5000))
    
    # Use debug=False for production
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    
    app.run(debug=debug_mode, host='0.0.0.0', port=port)

