#!/usr/bin/env python3
"""
Test script to verify n8n integration with Flask API
This simulates data coming from n8n automation server
"""

import requests
import json

# Test data that would come from n8n
n8n_test_data = {
    "structured_report": """
# Patient Medical Report

## Patient Information
- **Name**: John Doe
- **Age**: 45
- **Gender**: Male

## Chief Complaint
Patient presents with chest pain and shortness of breath.

## Assessment
1. **Cardiovascular**: Possible angina
2. **Respiratory**: Normal breathing patterns
3. **Psychological**: Patient appears anxious

## Recommendations
- Further cardiac evaluation
- Stress testing recommended
- Follow-up in 2 weeks
    """,
    
    "cardiologist": """
# Cardiologist Assessment

## Clinical Findings
- Elevated blood pressure: 150/95 mmHg
- ECG shows minor ST-segment changes
- Patient reports chest tightness during exertion

## Diagnosis
**Primary**: Hypertensive cardiovascular disease
**Secondary**: Possible stable angina

## Treatment Plan
1. Start ACE inhibitor therapy
2. Lifestyle modifications
3. Cardiac stress test within 1 week
    """,
    
    "psychologist": """
# Psychological Assessment

## Mental Status Examination
- Patient appears anxious and worried
- No signs of depression
- Good cognitive function

## Assessment
**Primary**: Anxiety related to health concerns
**Secondary**: Adjustment reaction to medical symptoms

## Recommendations
1. Relaxation techniques
2. Health education
3. Follow-up if anxiety persists
    """,
    
    "pulmonologist": """
# Pulmonology Assessment

## Respiratory Examination
- Clear lung sounds bilaterally
- Normal oxygen saturation (98%)
- No evidence of pulmonary disease

## Assessment
**Primary**: Normal respiratory function
**Secondary**: Shortness of breath likely cardiovascular in origin

## Recommendations
1. No pulmonary intervention needed
2. Focus on cardiovascular evaluation
    """,
    
    "final_summary": """
# Multidisciplinary Team Summary

## Consensus Diagnosis
**Primary**: Hypertensive cardiovascular disease with possible stable angina
**Secondary**: Health-related anxiety

## Integrated Treatment Plan
1. **Cardiovascular Management**
   - ACE inhibitor therapy
   - Cardiac stress testing
   - Blood pressure monitoring

2. **Psychological Support**
   - Anxiety management techniques
   - Patient education about condition

3. **Follow-up Care**
   - Cardiology appointment in 1 week
   - Primary care follow-up in 2 weeks
   - Psychology consultation if needed

## Prognosis
Good prognosis with appropriate management and lifestyle modifications.
    """
}

def test_n8n_integration():
    """Test the Flask API with n8n-style markdown data"""
    
    base_url = "http://127.0.0.1:5000"
    
    print("🔍 Testing n8n Integration with Flask API")
    print("=" * 50)
    
    # Test 1: Health Check
    print("\n1. Testing Health Endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False
    
    # Test 2: Generate PDF from n8n data
    print("\n2. Testing PDF Generation with n8n Data...")
    print(f"   Sending data with fields: {list(n8n_test_data.keys())}")
    try:
        response = requests.post(
            f"{base_url}/generate-pdf",
            json=n8n_test_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"   Response status: {response.status_code}")
        print(f"   Response headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            # Check if response is binary (PDF) or JSON
            content_type = response.headers.get('content-type', '')
            if 'application/pdf' in content_type:
                print(f"✅ PDF generation successful - received PDF file")
                print(f"   📄 Size: {len(response.content)} bytes")
                
                # Save the PDF to verify it works
                with open("test_output.pdf", "wb") as f:
                    f.write(response.content)
                print(f"   📍 Saved to: test_output.pdf")
                return True
            else:
                # JSON response
                result = response.json()
                print(f"✅ PDF generation successful")
                print(f"   📄 File: {result.get('filename', 'Unknown')}")
                print(f"   📍 Path: {result.get('path', 'Unknown')}")
                return True
        else:
            print(f"❌ PDF generation failed: {response.status_code}")
            print(f"   Response text: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ PDF generation error: {e}")
        print(f"   Response content: {response.text if 'response' in locals() else 'No response'}")
        return False

if __name__ == "__main__":
    success = test_n8n_integration()
    if success:
        print("\n🎉 n8n Integration Test PASSED!")
        print("Your Flask API is ready for n8n automation!")
    else:
        print("\n💥 n8n Integration Test FAILED!")
        print("Check the Flask API logs for details.")
