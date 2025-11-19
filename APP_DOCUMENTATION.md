# EcoScan - Clothing Sustainability Scanner

## Overview
EcoScan is a mobile application that uses AI-powered vision analysis to scan clothing items and provide detailed sustainability information including materials, longevity, recyclability, and environmental impact.

## Features

### 1. Smart Scanning
- Scan clothing labels for detailed fabric information
- Scan actual garments for visual material analysis
- Uses OpenAI GPT-4o Vision API for accurate analysis

### 2. Detailed Analysis
The app provides comprehensive information including:
- **Materials**: List of fabrics and materials identified
- **Longevity**: Expected lifespan with proper care
- **Recyclability**: How and where to recycle
- **Care Instructions**: Detailed care guidelines to maximize garment life
- **Environmental Impact**: Water usage, carbon footprint, chemical processing
- **Sustainability Score**: 1-10 rating with explanation

### 3. Scan History
- Save all scans to view later
- Delete unwanted scans
- Review past analyses

### 4. Eco-Themed Design
- Minimal, clean interface with green color palette
- Easy navigation between screens
- Mobile-optimized experience

## Technology Stack

### Frontend
- **Framework**: Expo / React Native
- **Navigation**: Expo Router (file-based routing)
- **Camera**: expo-camera
- **Storage**: AsyncStorage
- **UI**: React Native components with custom styling

### Backend
- **Framework**: FastAPI (Python)
- **Database**: MongoDB
- **AI Integration**: OpenAI GPT-4o via emergentintegrations library
- **API Key**: Emergent LLM Universal Key

### Key Libraries
- `emergentintegrations`: Custom library for LLM integrations
- `motor`: Async MongoDB driver
- `expo-camera`: Camera functionality
- `@react-native-async-storage/async-storage`: Local storage

## API Endpoints

### GET /api/
Health check endpoint

### POST /api/analyze-clothing
Analyze clothing image with AI
```json
{
  "image_base64": "base64_encoded_image",
  "scan_type": "label" | "garment"
}
```

### GET /api/scan-history
Retrieve all saved scans

### DELETE /api/scan/{scan_id}
Delete a specific scan

## App Structure

```
/app/frontend/app/
├── index.tsx          # Home screen
├── scan.tsx           # Camera/scanning screen
├── results.tsx        # Analysis results screen
└── history.tsx        # Scan history screen
```

## How to Use

1. **Home Screen**: 
   - Tap "Start Scanning" to begin
   - Or tap "View History" to see past scans

2. **Scanning**:
   - Grant camera permission when prompted
   - Position clothing label or garment in frame
   - Tap capture button
   - Select scan type (Label or Garment)
   - Tap "Analyze Sustainability"

3. **Results**:
   - Review detailed analysis
   - See sustainability score
   - Get care instructions
   - Learn about recyclability

4. **History**:
   - Browse past scans
   - Tap any scan to view details again
   - Swipe or tap delete to remove scans

## Environment Variables

### Backend (.env)
```
MONGO_URL=mongodb://localhost:27017
DB_NAME=test_database
EMERGENT_LLM_KEY=sk-emergent-0BfE04f1465E8E8B5C
```

### Frontend (.env)
```
EXPO_PUBLIC_BACKEND_URL=https://textile-checker.preview.emergentagent.com
```

## Color Palette
- Primary Green: #4CAF50
- Dark Green: #2E7D32
- Light Background: #F1F8E9
- Light Green: #E8F5E9
- White: #FFFFFF

## Database Schema

### scans Collection
```json
{
  "id": "uuid",
  "image_base64": "base64_string",
  "analysis": {
    "materials": ["cotton", "polyester"],
    "longevity": "5-10 years with proper care",
    "recyclability": "Recyclable at textile facilities",
    "care_instructions": "Machine wash cold, tumble dry low",
    "environmental_impact": "Moderate impact...",
    "sustainability_score": "7/10 - Good sustainability..."
  },
  "scan_type": "label",
  "timestamp": "2025-01-19T11:23:37Z"
}
```

## Testing

Backend testing completed and all endpoints verified:
- ✅ Health check
- ✅ Scan history retrieval
- ✅ Clothing analysis with OpenAI Vision
- ✅ Scan deletion

## Preview URLs

- **Web Preview**: https://textile-checker.preview.emergentagent.com
- **Backend API**: https://textile-checker.preview.emergentagent.com/api

## Notes

- Images are stored as base64 in MongoDB for easy retrieval and display
- The app uses OpenAI's GPT-4o model for vision analysis
- Camera permissions are required for scanning functionality
- All API calls include proper error handling
- The app works on both iOS and Android devices
