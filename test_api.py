"""
Flask API Test Script for Medical Diagnostics
This script demonstrates how to use the Flask API endpoints
"""

import requests
import json
import os

# API base URL
BASE_URL = "http://localhost:5000"

def test_api():
    """Test the complete API workflow"""
    
    print("🏥 Testing Medical Diagnostics API\n")
    
    # Step 1: Health check
    print("1. Health Check...")
    response = requests.get(f"{BASE_URL}/health")
    if response.status_code == 200:
        print("✅ API is healthy")
        print(f"   Response: {response.json()}\n")
    else:
        print("❌ API health check failed")
        return
    
    # Step 2: Upload PDF
    print("2. Uploading PDF...")
    pdf_path = "case-report-.pdf"  # Update with your PDF path
    
    if not os.path.exists(pdf_path):
        print(f"❌ PDF file not found: {pdf_path}")
        return
    
    with open(pdf_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(f"{BASE_URL}/upload-pdf", files=files)
    
    if response.status_code == 200:
        upload_result = response.json()
        uploaded_path = upload_result['file_path']
        print(f"✅ PDF uploaded successfully: {uploaded_path}\n")
    else:
        print(f"❌ PDF upload failed: {response.json()}")
        return
    
    # Step 3: Extract text
    print("3. Extracting text...")
    response = requests.post(f"{BASE_URL}/extract-text", 
                           json={"path": uploaded_path})
    
    if response.status_code == 200:
        extract_result = response.json()
        raw_text = extract_result['raw_text']
        print(f"✅ Text extracted ({len(raw_text)} characters)\n")
    else:
        print(f"❌ Text extraction failed: {response.json()}")
        return
    
    # Step 4: Structure report
    print("4. Structuring report...")
    response = requests.post(f"{BASE_URL}/structure-report", 
                           json={"text": raw_text})
    
    if response.status_code == 200:
        structure_result = response.json()
        structured_report = structure_result['structured_report']
        print("✅ Report structured successfully\n")
    else:
        print(f"❌ Report structuring failed: {response.json()}")
        return
    
    # Step 5: Run agents
    print("5. Running AI agents...")
    agents = ['cardiologist', 'psychologist', 'pulmonologist']
    agent_results = {}
    
    for agent in agents:
        response = requests.post(f"{BASE_URL}/run-agent/{agent}", 
                               json={"text": structured_report})
        
        if response.status_code == 200:
            agent_result = response.json()
            agent_results[agent] = agent_result['assessment']
            print(f"   ✅ {agent.title()} assessment completed")
        else:
            print(f"   ❌ {agent.title()} assessment failed: {response.json()}")
            return
    
    print()
    
    # Step 6: Generate multidisciplinary summary
    print("6. Generating multidisciplinary summary...")
    response = requests.post(f"{BASE_URL}/multidisciplinary-summary", 
                           json=agent_results)
    
    if response.status_code == 200:
        summary_result = response.json()
        final_summary = summary_result['summary']
        print("✅ Multidisciplinary summary generated\n")
    else:
        print(f"❌ Summary generation failed: {response.json()}")
        return
    
    # Step 7: Generate PDF
    print("7. Generating final PDF...")
    pdf_data = {
        "structured_report": structured_report,
        "cardiologist": agent_results['cardiologist'],
        "psychologist": agent_results['psychologist'],
        "pulmonologist": agent_results['pulmonologist'],
        "final_summary": final_summary
    }
    
    response = requests.post(f"{BASE_URL}/generate-pdf", json=pdf_data)
    
    if response.status_code == 200:
        # Save the PDF
        with open("api_generated_report.pdf", "wb") as f:
            f.write(response.content)
        print("✅ PDF generated successfully: api_generated_report.pdf\n")
    else:
        print(f"❌ PDF generation failed: {response.json()}")
        return
    
    # Alternative: Test complete processing endpoint
    print("8. Testing complete processing endpoint...")
    response = requests.post(f"{BASE_URL}/process-complete", 
                           json={"pdf_path": uploaded_path})
    
    if response.status_code == 200:
        with open("api_complete_report.pdf", "wb") as f:
            f.write(response.content)
        print("✅ Complete processing successful: api_complete_report.pdf\n")
    else:
        print(f"❌ Complete processing failed: {response.json()}")
    
    print("🎉 API testing completed successfully!")

if __name__ == "__main__":
    test_api()
