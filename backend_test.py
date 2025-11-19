#!/usr/bin/env python3
"""
Backend API Testing for Clothing Sustainability Scanner
Tests all backend endpoints with real data
"""

import requests
import json
import base64
import os
from PIL import Image, ImageDraw
import io
import time

# Get backend URL from frontend env
BACKEND_URL = "https://textile-checker.preview.emergentagent.com/api"

def create_test_clothing_label_image():
    """Create a realistic clothing label image for testing"""
    # Create a 400x300 image with white background
    img = Image.new('RGB', (400, 300), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw a clothing label with text
    draw.rectangle([20, 20, 380, 280], outline='black', width=2)
    draw.rectangle([30, 30, 370, 270], outline='gray', width=1)
    
    # Add label text (simulating a clothing label)
    draw.text((50, 50), "CARE LABEL", fill='black')
    draw.text((50, 80), "100% Cotton", fill='black')
    draw.text((50, 110), "Machine wash cold", fill='black')
    draw.text((50, 140), "Tumble dry low", fill='black')
    draw.text((50, 170), "Do not bleach", fill='black')
    draw.text((50, 200), "Iron medium heat", fill='black')
    draw.text((50, 230), "Made in USA", fill='black')
    
    # Convert to base64
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG')
    img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    return img_base64

def create_test_garment_image():
    """Create a realistic garment image for testing"""
    # Create a 400x400 image with light background
    img = Image.new('RGB', (400, 400), color='lightblue')
    draw = ImageDraw.Draw(img)
    
    # Draw a simple t-shirt shape
    # Body
    draw.rectangle([150, 150, 250, 350], fill='navy', outline='darkblue', width=2)
    # Sleeves
    draw.rectangle([100, 150, 150, 220], fill='navy', outline='darkblue', width=2)
    draw.rectangle([250, 150, 300, 220], fill='navy', outline='darkblue', width=2)
    # Neck
    draw.ellipse([180, 130, 220, 170], fill='lightblue', outline='darkblue', width=2)
    
    # Add some texture lines
    for i in range(160, 340, 20):
        draw.line([160, i, 240, i], fill='lightgray', width=1)
    
    # Convert to base64
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG')
    img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    return img_base64

def test_health_check():
    """Test GET /api/ endpoint"""
    print("🔍 Testing GET /api/ (Health Check)")
    try:
        response = requests.get(f"{BACKEND_URL}/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            data = response.json()
            if "message" in data and "Clothing Sustainability Scanner API" in data["message"]:
                print("✅ Health check passed")
                return True
            else:
                print("❌ Health check failed - unexpected response format")
                return False
        else:
            print(f"❌ Health check failed - status code {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check failed - error: {str(e)}")
        return False

def test_scan_history_empty():
    """Test GET /api/scan-history when empty"""
    print("\n🔍 Testing GET /api/scan-history (Empty)")
    try:
        response = requests.get(f"{BACKEND_URL}/scan-history")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                print(f"✅ Scan history returned list with {len(data)} items")
                return True, len(data)
            else:
                print("❌ Scan history failed - not a list")
                return False, 0
        else:
            print(f"❌ Scan history failed - status code {response.status_code}")
            return False, 0
    except Exception as e:
        print(f"❌ Scan history failed - error: {str(e)}")
        return False, 0

def test_analyze_clothing(scan_type, image_base64):
    """Test POST /api/analyze-clothing endpoint"""
    print(f"\n🔍 Testing POST /api/analyze-clothing (scan_type: {scan_type})")
    try:
        payload = {
            "image_base64": image_base64,
            "scan_type": scan_type
        }
        
        print("Sending request to OpenAI Vision API...")
        response = requests.post(f"{BACKEND_URL}/analyze-clothing", json=payload, timeout=60)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response keys: {list(data.keys())}")
            
            # Check required fields
            required_fields = ["success", "scan_id", "analysis"]
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                print(f"❌ Missing required fields: {missing_fields}")
                return False, None
            
            # Check analysis structure
            analysis = data["analysis"]
            required_analysis_fields = [
                "materials", "longevity", "recyclability", 
                "care_instructions", "environmental_impact", "sustainability_score"
            ]
            missing_analysis_fields = [field for field in required_analysis_fields if field not in analysis]
            
            if missing_analysis_fields:
                print(f"❌ Missing analysis fields: {missing_analysis_fields}")
                return False, None
            
            print("✅ Analysis completed successfully")
            print(f"Scan ID: {data['scan_id']}")
            print(f"Materials: {analysis['materials']}")
            print(f"Sustainability Score: {analysis['sustainability_score']}")
            
            return True, data["scan_id"]
        else:
            print(f"❌ Analysis failed - status code {response.status_code}")
            try:
                error_data = response.json()
                print(f"Error details: {error_data}")
            except:
                print(f"Error response: {response.text}")
            return False, None
            
    except requests.exceptions.Timeout:
        print("❌ Analysis failed - request timeout (60s)")
        return False, None
    except Exception as e:
        print(f"❌ Analysis failed - error: {str(e)}")
        return False, None

def test_scan_history_with_data():
    """Test GET /api/scan-history after adding data"""
    print("\n🔍 Testing GET /api/scan-history (With Data)")
    try:
        response = requests.get(f"{BACKEND_URL}/scan-history")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Number of scans: {len(data)}")
            
            if len(data) > 0:
                # Check structure of first scan
                scan = data[0]
                required_fields = ["id", "image_base64", "analysis", "scan_type", "timestamp"]
                missing_fields = [field for field in required_fields if field not in scan]
                
                if missing_fields:
                    print(f"❌ Missing scan fields: {missing_fields}")
                    return False, []
                
                print("✅ Scan history with data retrieved successfully")
                return True, [scan["id"] for scan in data]
            else:
                print("⚠️ No scans found in history")
                return True, []
        else:
            print(f"❌ Scan history failed - status code {response.status_code}")
            return False, []
    except Exception as e:
        print(f"❌ Scan history failed - error: {str(e)}")
        return False, []

def test_delete_scan(scan_id):
    """Test DELETE /api/scan/{scan_id} endpoint"""
    print(f"\n🔍 Testing DELETE /api/scan/{scan_id}")
    try:
        response = requests.delete(f"{BACKEND_URL}/scan/{scan_id}")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success") and "deleted" in data.get("message", "").lower():
                print("✅ Scan deleted successfully")
                return True
            else:
                print("❌ Delete failed - unexpected response")
                return False
        elif response.status_code == 404:
            print("⚠️ Scan not found (already deleted or invalid ID)")
            return True  # This is acceptable
        else:
            print(f"❌ Delete failed - status code {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Delete failed - error: {str(e)}")
        return False

def main():
    """Run all backend tests"""
    print("=" * 60)
    print("🧪 CLOTHING SUSTAINABILITY SCANNER - BACKEND API TESTS")
    print("=" * 60)
    print(f"Backend URL: {BACKEND_URL}")
    
    # Test results tracking
    results = {
        "health_check": False,
        "scan_history_empty": False,
        "analyze_label": False,
        "analyze_garment": False,
        "scan_history_with_data": False,
        "delete_scan": False
    }
    
    scan_ids = []
    
    # 1. Test health check
    results["health_check"] = test_health_check()
    
    # 2. Test empty scan history
    success, initial_count = test_scan_history_empty()
    results["scan_history_empty"] = success
    
    # 3. Create test images
    print("\n📸 Creating test images...")
    label_image = create_test_clothing_label_image()
    garment_image = create_test_garment_image()
    print("✅ Test images created")
    
    # 4. Test analyze clothing with label
    success, scan_id = test_analyze_clothing("label", label_image)
    results["analyze_label"] = success
    if scan_id:
        scan_ids.append(scan_id)
    
    # 5. Test analyze clothing with garment
    success, scan_id = test_analyze_clothing("garment", garment_image)
    results["analyze_garment"] = success
    if scan_id:
        scan_ids.append(scan_id)
    
    # 6. Test scan history with data
    success, all_scan_ids = test_scan_history_with_data()
    results["scan_history_with_data"] = success
    
    # 7. Test delete scans
    if scan_ids:
        delete_success = True
        for scan_id in scan_ids:
            if not test_delete_scan(scan_id):
                delete_success = False
        results["delete_scan"] = delete_success
    else:
        print("\n⚠️ No scan IDs to delete")
        results["delete_scan"] = True  # No scans to delete is OK
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name.replace('_', ' ').title()}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Backend API is working correctly.")
    else:
        print("⚠️ Some tests failed. Check the details above.")
    
    return results

if __name__ == "__main__":
    main()