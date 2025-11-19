import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  Dimensions,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { LinearGradient } from 'expo-linear-gradient';

const { width } = Dimensions.get('window');

export default function HomeScreen() {
  const router = useRouter();

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.scrollContent}>
        <View style={styles.hero}>
          <View style={styles.iconContainer}>
            <Ionicons name="leaf" size={60} color="#4CAF50" />
          </View>
          <Text style={styles.title}>EcoScan</Text>
          <Text style={styles.subtitle}>Sustainable Fashion Intelligence</Text>
          <Text style={styles.description}>
            Scan clothing labels and garments to discover materials, longevity, and environmental impact
          </Text>
        </View>

        <View style={styles.featuresContainer}>
          <View style={styles.featureCard}>
            <Ionicons name="camera" size={32} color="#4CAF50" />
            <Text style={styles.featureTitle}>Smart Scanning</Text>
            <Text style={styles.featureText}>
              AI-powered analysis of clothing labels and garments
            </Text>
          </View>

          <View style={styles.featureCard}>
            <Ionicons name="leaf" size={32} color="#4CAF50" />
            <Text style={styles.featureTitle}>Sustainability Score</Text>
            <Text style={styles.featureText}>
              Get detailed environmental impact assessments
            </Text>
          </View>

          <View style={styles.featureCard}>
            <Ionicons name="time" size={32} color="#4CAF50" />
            <Text style={styles.featureTitle}>Longevity Insights</Text>
            <Text style={styles.featureText}>
              Learn about durability and proper care
            </Text>
          </View>

          <View style={styles.featureCard}>
            <Ionicons name="sync" size={32} color="#4CAF50" />
            <Text style={styles.featureTitle}>Recyclability Info</Text>
            <Text style={styles.featureText}>
              Discover how and where to recycle your clothing
            </Text>
          </View>
        </View>

        <View style={styles.actions}>
          <TouchableOpacity
            style={styles.primaryButton}
            onPress={() => router.push('/scan')}
            activeOpacity={0.8}
          >
            <Ionicons name="scan" size={24} color="#fff" />
            <Text style={styles.primaryButtonText}>Start Scanning</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={styles.secondaryButton}
            onPress={() => router.push('/history')}
            activeOpacity={0.8}
          >
            <Ionicons name="list" size={24} color="#4CAF50" />
            <Text style={styles.secondaryButtonText}>View History</Text>
          </TouchableOpacity>
        </View>

        <View style={styles.footer}>
          <Text style={styles.footerText}>
            Making sustainable fashion choices, one scan at a time
          </Text>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F1F8E9',
  },
  scrollContent: {
    flexGrow: 1,
  },
  hero: {
    alignItems: 'center',
    paddingVertical: 40,
    paddingHorizontal: 24,
  },
  iconContainer: {
    width: 120,
    height: 120,
    borderRadius: 60,
    backgroundColor: '#E8F5E9',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 20,
  },
  title: {
    fontSize: 48,
    fontWeight: 'bold',
    color: '#2E7D32',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 18,
    color: '#4CAF50',
    fontWeight: '600',
    marginBottom: 16,
  },
  description: {
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
    lineHeight: 24,
    paddingHorizontal: 16,
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
    fontSize: 14,
    color: '#666',
    lineHeight: 20,
  },
  actions: {
    paddingHorizontal: 16,
    gap: 12,
    marginBottom: 32,
  },
  primaryButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#4CAF50',
    paddingVertical: 18,
    borderRadius: 16,
    gap: 12,
    shadowColor: '#4CAF50',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 5,
  },
  primaryButtonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '600',
  },
  secondaryButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#fff',
    paddingVertical: 18,
    borderRadius: 16,
    borderWidth: 2,
    borderColor: '#4CAF50',
    gap: 12,
  },
  secondaryButtonText: {
    color: '#4CAF50',
    fontSize: 18,
    fontWeight: '600',
  },
  footer: {
    paddingHorizontal: 32,
    paddingBottom: 32,
    alignItems: 'center',
  },
  footerText: {
    fontSize: 14,
    color: '#999',
    textAlign: 'center',
    fontStyle: 'italic',
  },
});