import React, { useState, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Image,
  Alert,
  ScrollView,
  ActivityIndicator,
  Platform,
  Button
} from 'react-native';
import { Picker } from '@react-native-picker/picker';
import { CameraView, useCameraPermissions } from 'expo-camera';
import { Ionicons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import * as ImagePicker from 'expo-image-picker';

const BACKEND_URL = 'http://127.0.0.1:8000';

export default function ScanScreen() {
  const [permission, requestPermission] = useCameraPermissions();
  const [capturedImage, setCapturedImage] = useState<string | null>(null);
  const [scanType, setScanType] = useState<'label' | 'garment'>('label');
  const [analyzing, setAnalyzing] = useState(false);
  const [selectedClothing, setSelectedClothing] = useState<string>('sweater');
  const cameraRef = useRef<any>(null);
  const router = useRouter();

  if (!permission) {
    return (
      <SafeAreaView style={styles.container}>
        <ActivityIndicator size="large" color="#4CAF50" />
      </SafeAreaView>
    );
  }

  if (!permission.granted) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.permissionContainer}>
          <Ionicons name="camera-outline" size={80} color="#4CAF50" />
          <Text style={styles.permissionText}>Camera Access Required</Text>
          <Text style={styles.permissionSubtext}>
            We need camera access to scan clothing items
          </Text>
          <TouchableOpacity style={styles.permissionButton} onPress={requestPermission}>
            <Text style={styles.permissionButtonText}>Grant Permission</Text>
          </TouchableOpacity>
        </View>
      </SafeAreaView>
    );
  }

  const takePicture = async () => {
    if (cameraRef.current) {
      try {
        const photo = await cameraRef.current.takePictureAsync({
          quality: 0.8,
          base64: true,
        });

        setCapturedImage(`${photo.base64}`);
      } catch (error) {
        console.error('Error taking picture:', error);
        Alert.alert('Error', 'Failed to take picture');
      }
    }
  };

  const uploadPicture = async () => {
    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ["images"], 
      base64: true
    });
    
    if (!result.canceled && result.assets && result.assets.length > 0) {
      const asset = result.assets[0];
      if (asset.base64) {
        setCapturedImage(`data:image/jpeg;base64,${asset.base64}`);
      } else {
        console.warn("No base64 data returned from picker");
      }
    }
  };

  const analyzeImage = async () => {
    if (!capturedImage) return;

    console.log("Sending data to backend..");
    console.log(selectedClothing);

    setAnalyzing(true);
    try {
      const response = await fetch(`${BACKEND_URL}/api/analyze-clothing`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          image_base64: capturedImage,
          scan_type: scanType,
          clothing_type: selectedClothing
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to analyze image');
      }

      const data = await response.json();
      
      console.log(data);

      // Navigate to results screen with data
      router.push({
        pathname: '/results',
        params: {
          analysisResults: JSON.stringify(data),
        },
      });
    } catch (error) {
      console.error('Error analyzing image:', error);
      Alert.alert('Error', 'Failed to analyze clothing. Please try again.');
    } finally {
      setAnalyzing(false);
    }
  };

  const retake = () => {
    setCapturedImage(null);
  };

  if (capturedImage) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.header}>
          <TouchableOpacity onPress={retake} style={styles.backButton}>
            <Ionicons name="arrow-back" size={24} color="#2E7D32" />
          </TouchableOpacity>
          <Text style={styles.headerTitle}>Review Photo</Text>
        </View>

        <ScrollView contentContainerStyle={styles.previewContainer}>
          <Image source={{ uri: capturedImage }} style={styles.previewImage} />

          <View style={styles.scanTypeContainer}>
            <Text style={styles.scanTypeLabel}>What Clothing does this Label belong to?</Text>
            <View style={styles.picker}>
                <Picker
                  selectedValue={selectedClothing}
                  onValueChange={(value, itemIndex) => setSelectedClothing(value)}
                  style={styles.picker}
                >
                  <Picker.Item label="Sweater" value="sweater" />
                  <Picker.Item label="Jacket" value="jacket" />
                  <Picker.Item label="Jeans" value="jeans" />
                  <Picker.Item label="Shorts" value="shorts" />
                  <Picker.Item label="Pants" value="pants" />
                  <Picker.Item label="Dress" value="dress" />
                  <Picker.Item label="Skirt" value="skirts" />
                </Picker>
              </View>
          </View>

          <TouchableOpacity
            style={[styles.analyzeButton, analyzing && styles.analyzeButtonDisabled]}
            onPress={analyzeImage}
            disabled={analyzing}
          >
            {analyzing ? (
              <ActivityIndicator size="small" color="#fff" />
            ) : (
              <>
                <Ionicons name="sparkles" size={24} color="#fff" />
                <Text style={styles.analyzeButtonText}>Analyze Sustainability</Text>
              </>
            )}
          </TouchableOpacity>
        </ScrollView>
      </SafeAreaView>
    );
  } 

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
          <Ionicons name="arrow-back" size={24} color="#2E7D32" />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Scan Clothing</Text>
      </View>

      <View style={styles.cameraContainer}>
        <CameraView style={styles.camera} ref={cameraRef} facing="back">
          <View style={styles.cameraOverlay}>
            <View style={styles.scanFrame} />
            <Text style={styles.instructionText}>
              Position clothing or label within the frame
            </Text>
          </View>
        </CameraView>
      </View>

      <View style={styles.controls}>
        <TouchableOpacity style={styles.captureButton} onPress={takePicture}>
          <View style={styles.captureButtonInner} />
        </TouchableOpacity>
      </View>

      <View>
        <Button title="Pick Image" onPress={uploadPicture} />
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F1F8E9',
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingVertical: 12,
    backgroundColor: '#fff',
    borderBottomWidth: 1,
    borderBottomColor: '#E0E0E0',
  },
  backButton: {
    padding: 8,
  },
  headerTitle: {
    fontSize: 20,
    fontWeight: '600',
    color: '#2E7D32',
    marginLeft: 16,
  },
  permissionContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 32,
  },
  permissionText: {
    fontSize: 24,
    fontWeight: '600',
    color: '#2E7D32',
    marginTop: 24,
    textAlign: 'center',
  },
  permissionSubtext: {
    fontSize: 16,
    color: '#666',
    marginTop: 12,
    textAlign: 'center',
  },
  permissionButton: {
    backgroundColor: '#4CAF50',
    paddingHorizontal: 32,
    paddingVertical: 16,
    borderRadius: 12,
    marginTop: 32,
  },
  permissionButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  picker:{
    height: 30,
    fontSize: 16    
  },
  cameraContainer: {
    flex: 1,
  },
  camera: {
    flex: 1,
  },
  cameraOverlay: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  scanFrame: {
    width: 280,
    height: 280,
    borderWidth: 3,
    borderColor: '#4CAF50',
    borderRadius: 16,
    backgroundColor: 'transparent',
  },
  instructionText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
    marginTop: 24,
    textAlign: 'center',
    paddingHorizontal: 32,
    backgroundColor: 'rgba(0,0,0,0.5)',
    paddingVertical: 12,
    borderRadius: 8,
  },
  controls: {
    padding: 32,
    alignItems: 'center',
    backgroundColor: '#fff',
  },
  captureButton: {
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: '#fff',
    borderWidth: 4,
    borderColor: '#4CAF50',
    justifyContent: 'center',
    alignItems: 'center',
  },
  captureButtonInner: {
    width: 64,
    height: 64,
    borderRadius: 32,
    backgroundColor: '#4CAF50',
  },
  previewContainer: {
    padding: 16,
  },
  previewImage: {
    width: '100%',
    height: 400,
    borderRadius: 12,
    resizeMode: 'contain',
  },
  scanTypeContainer: {
    marginTop: 24,
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
  },
  scanTypeLabel: {
    fontSize: 18,
    fontWeight: '600',
    color: '#2E7D32',
    marginBottom: 12,
  },
  scanTypeButtons: {
    flexDirection: 'row',
    gap: 12,
  },
  scanTypeButton: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 16,
    borderRadius: 12,
    borderWidth: 2,
    borderColor: '#4CAF50',
    backgroundColor: '#fff',
    gap: 8,
  },
  scanTypeButtonActive: {
    backgroundColor: '#4CAF50',
  },
  scanTypeButtonText: {
    fontSize: 14,
    fontWeight: '600',
    color: '#4CAF50',
  },
  scanTypeButtonTextActive: {
    color: '#fff',
  },
  analyzeButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#4CAF50',
    padding: 18,
    borderRadius: 12,
    marginTop: 24,
    gap: 8,
  },
  analyzeButtonDisabled: {
    opacity: 0.6,
  },
  analyzeButtonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '600',
  },
});