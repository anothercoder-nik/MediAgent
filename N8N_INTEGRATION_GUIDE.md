# n8n Integration Guide for Medical Diagnostics API

## Overview
This Flask API is designed to work seamlessly with n8n automation workflows for processing medical diagnostic reports and generating PDF summaries.

## API Endpoints

### 1. Health Check
- **URL**: `GET /health`
- **Purpose**: Verify API is running
- **Response**: JSON with service status

### 2. Upload PDF
- **URL**: `POST /upload-pdf`
- **Purpose**: Upload medical report PDF for processing
- **Body**: Multipart form with PDF file
- **Response**: JSON with upload confirmation and file path

### 3. Extract Text from PDF
- **URL**: `POST /extract-text`
- **Purpose**: Extract raw text from uploaded PDF
- **Body**: JSON `{"pdf_path": "path_to_pdf"}`
- **Response**: JSON with extracted text

### 4. Structure Medical Report
- **URL**: `POST /structure-report`
- **Purpose**: Structure raw text into organized medical report
- **Body**: JSON `{"raw_text": "extracted_text"}`
- **Response**: JSON with structured report

### 5. Generate AI Agent Assessments
Individual specialist endpoints:
- **Cardiologist**: `POST /cardiologist`
- **Psychologist**: `POST /psychologist` 
- **Pulmonologist**: `POST /pulmonologist`

**Body**: JSON `{"structured_report": "structured_text"}`
**Response**: JSON with specialist assessment

### 6. Generate Multidisciplinary Summary
- **URL**: `POST /multidisciplinary-summary`
- **Purpose**: Create unified summary from all specialist assessments
- **Body**: JSON with all specialist reports
- **Response**: JSON with final summary

### 7. Generate Final PDF Report ⭐ **Main n8n Endpoint**
- **URL**: `POST /generate-pdf`
- **Purpose**: Create final PDF report from all assessments
- **Body**: JSON with required fields (see below)
- **Response**: PDF file download

## n8n Integration - Main Endpoint

### Required JSON Structure for `/generate-pdf`

```json
{
    "structured_report": "# Patient Medical Report\n\n## Patient Information\n- **Name**: John Doe\n...",
    "cardiologist": "# Cardiologist Assessment\n\n## Clinical Findings\n...",
    "psychologist": "# Psychological Assessment\n\n## Mental Status\n...",
    "pulmonologist": "# Pulmonology Assessment\n\n## Respiratory Examination\n...",
    "final_summary": "# Multidisciplinary Team Summary\n\n## Consensus Diagnosis\n..."
}
```

### Field Requirements
- **structured_report**: Initial patient report (Markdown format)
- **cardiologist**: Cardiologist assessment (Markdown format)
- **psychologist**: Psychologist assessment (Markdown format)  
- **pulmonologist**: Pulmonologist assessment (Markdown format)
- **final_summary**: Unified team summary (Markdown format)

### Markdown Support
All text fields support full Markdown formatting:
- Headers (`#`, `##`, `###`)
- Bold text (`**bold**`)
- Lists (`-`, `1.`)
- Tables
- Emphasis (`*italic*`)

## n8n Workflow Example

1. **HTTP Request Node**: POST to `/generate-pdf`
2. **Headers**: `Content-Type: application/json`
3. **Body**: JSON object with all 5 required fields
4. **Response**: PDF file that can be saved or sent via email

## Testing

Use the included `test_n8n_integration.py` script to verify the API works correctly:

```bash
python test_n8n_integration.py
```

## Dependencies

Install required packages:
```bash
pip install -r requirements_api.txt
```

## Running the API

```bash
python app.py
```

The API will be available at:
- Local: `http://127.0.0.1:5000`
- Network: `http://[your-ip]:5000`

## Error Handling

The API returns appropriate HTTP status codes:
- `200`: Success
- `400`: Bad request (missing/invalid data)
- `404`: File not found
- `500`: Server error

All errors include JSON response with error details.

## Security Notes

- This is a development server - use a production WSGI server for deployment
- Configure proper authentication for production use
- Validate and sanitize all inputs in production
