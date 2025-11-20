import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Image,
  ScrollView,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useRouter, useLocalSearchParams } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';

const BACKEND_URL = 'http://127.0.0.1:8000';

export default function ResultsScreen() {
  const router = useRouter();
  const params = useLocalSearchParams();
  const analysis = JSON.parse(params.analysisResults as string); 

  if (!analysis) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.errorContainer}>
          <Ionicons name="alert-circle" size={64} color="#F44336" />
          <Text style={styles.errorText}>No analysis data found</Text>
          <TouchableOpacity style={styles.button} onPress={() => router.back()}>
            <Text style={styles.buttonText}>Go Back</Text>
          </TouchableOpacity>
        </View>
      </SafeAreaView>
    );
  }
  
  const formatted_material_compose = analysis["material_composition"]
  .map((item: { material_name: string; environmental_consequence: string }) => 
    `${item.material_name} - ${item.environmental_consequence}`
  )
  .join("\n");

  const is_sustainable = analysis["final_decision"]

  let sustainability_string = "Your clothing item is environmentally sustainable ✅"

  if(!is_sustainable) {
    sustainability_string = "Your clothing item is not environmentally sustainable ❌"
  }

  const getScoreColor = (score: string) => {
    const numScore = parseInt(score);
    if (numScore >= 8) return '#4CAF50';
    if (numScore >= 5) return '#FF9800';
    return '#F44336';
  };

  const searchAlternatives = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/api/search-alternatives`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          clothing_type: analysis["clothing_type"],
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to process request');
      }

      const data = await response.json();
      console.log(data);

      // Navigate to results screen with data
      router.push({
        pathname: '/alternatives',
        params: {
          analysisResults: JSON.stringify(data),
        },
      });
    } catch (error) {
      console.error('Error analyzing image:', error);
      //Alert.alert('Error', 'Failed to analyze clothing. Please try again.');
    } 
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
          <Ionicons name="arrow-back" size={24} color="#2E7D32" />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Analysis Results</Text>
      </View>

      <ScrollView contentContainerStyle={styles.scrollContent}>
        <View style={styles.featuresContainer}>
            <View style={styles.featureCard}>
              <Ionicons name="leaf" size={32} color="#4CAF50" />
              <Text style={styles.featureTitle}>Carbon Footprint</Text>
              <Text style={styles.featureText}>
                {analysis["carbon_footprint"]}
              </Text>
            </View>

            <View style={styles.featureCard}>
              <Ionicons name="shirt" size={32} color="#4CAF50" />
              <Text style={styles.featureTitle}>Material Composition</Text>
              <Text style={styles.featureText}>
                {formatted_material_compose}
              </Text>
            </View>

            <View style={styles.featureCard}>
              <Ionicons name="flag" size={32} color="#4CAF50" />
              <Text style={styles.featureTitle}>Country of Origin</Text>
              <Text style={styles.featureText}>
                {analysis["country_origin"]}
              </Text>
            </View>

            <View style={styles.featureCard}>
              <Ionicons name="time" size={32} color="#4CAF50" />
              <Text style={styles.featureTitle}>Expected Durability</Text>
              <Text style={styles.featureText}>
                {analysis["expected_durability"]}
              </Text>
            </View>

            <View style={styles.featureCard}>
              <Ionicons name="arrow-forward-outline" size={32} color="#4CAF50" />
              <Text style={styles.featureTitle}>Final Verdict</Text>
              <Text style={styles.featureText}>
                {sustainability_string}
              </Text>
            </View>

            <View style={styles.featureCard}>
              <Ionicons name="sync" size={32} color="#4CAF50" />
              <Text style={styles.featureTitle}>Advice</Text>
              <Text style={styles.featureText}>
                {analysis["sustainable_tips"][0]}{"\n"}
                {analysis["sustainable_tips"][1]}{"\n"}
                {analysis["sustainable_tips"][2]}                
              </Text>
            </View>
          </View>

          {!is_sustainable && (
            <View style={styles.actions}>
            <TouchableOpacity
              style={styles.primaryButton}
              onPress={searchAlternatives}
              activeOpacity={0.8}
            >
              <Ionicons name="search-outline" size={24} color="#fff" />
              <Text style={styles.primaryButtonText}>Search for Alternatives</Text>
            </TouchableOpacity>
          </View>
          )}
        </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F1F8E9',
  },
  featuresContainer: {
    paddingHorizontal: 16,
    paddingVertical: 24,
  },
  featureCard: {
    backgroundColor: '#fff',
    borderRadius: 16,
    padding: 20,
    marginBottom: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 3,
  },
  featureTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#2E7D32',
    marginTop: 12,
    marginBottom: 8,
  },
  featureText: {
    fontSize: 16,
    color: '#474747',
    lineHeight: 20,
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
  content: {
    padding: 16,
  },
  image: {
    width: '100%',
    height: 200,
    borderRadius: 12,
    resizeMode: 'cover',
    marginBottom: 16,
  },
  badge: {
    flexDirection: 'row',
    alignItems: 'center',
    alignSelf: 'flex-start',
    backgroundColor: '#E8F5E9',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 16,
    marginBottom: 16,
    gap: 6,
  },
  badgeText: {
    color: '#4CAF50',
    fontSize: 14,
    fontWeight: '600',
  },
  scoreCard: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 24,
    alignItems: 'center',
    marginBottom: 16,
    borderWidth: 2,
    borderColor: '#E0E0E0',
  },
  scoreLabel: {
    fontSize: 16,
    color: '#666',
    marginBottom: 8,
  },
  scoreValue: {
    fontSize: 36,
    fontWeight: 'bold',
  },
  section: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
  },
  sectionHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
    gap: 8,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#2E7D32',
  },
  sectionContent: {
    fontSize: 15,
    color: '#333',
    lineHeight: 22,
  },
  scrollContent: {
    flexGrow: 1,
  },
  materialsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 8,
  },
  materialChip: {
    backgroundColor: '#E8F5E9',
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 20,
    borderWidth: 1,
    borderColor: '#4CAF50',
  },
  materialText: {
    color: '#2E7D32',
    fontSize: 14,
    fontWeight: '500',
  },
  actions: {
    marginTop: 0,
    marginBottom: 16,
    marginHorizontal: 16,
    gap: 4,
  },
  primaryButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#4CAF50',
    padding: 16,
    borderRadius: 12,
    gap: 8,
  },
  primaryButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  secondaryButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#fff',
    padding: 16,
    borderRadius: 12,
    borderWidth: 2,
    borderColor: '#4CAF50',
    gap: 8,
  },
  secondaryButtonText: {
    color: '#4CAF50',
    fontSize: 16,
    fontWeight: '600',
  },
  errorContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 32,
  },
  errorText: {
    fontSize: 18,
    color: '#666',
    marginTop: 16,
    marginBottom: 24,
  },
  button: {
    backgroundColor: '#4CAF50',
    paddingHorizontal: 32,
    paddingVertical: 16,
    borderRadius: 12,
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
});