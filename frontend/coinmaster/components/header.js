import React, { useState, useEffect } from 'react';
import { Text, View, StyleSheet, TouchableOpacity } from 'react-native';
import * as SplashScreen from 'expo-splash-screen';
import { useFonts, Jomhuria_400Regular } from '@expo-google-fonts/jomhuria';
import { JollyLodger_400Regular } from '@expo-google-fonts/jolly-lodger';
import { MaterialIcons, FontAwesome5 } from '@expo/vector-icons';

SplashScreen.preventAutoHideAsync(); // Prevent the splash screen from auto-hiding

const HeaderComponent = () => {
  const [fontsLoaded] = useFonts({
    Jomhuria_400Regular,
    JollyLodger_400Regular,
  });

  useEffect(() => {
    if (fontsLoaded) {
      SplashScreen.hideAsync(); // Hide the splash screen once fonts are loaded
    }
  }, [fontsLoaded]);

  if (!fontsLoaded) {
    return null; // Render nothing while fonts are loading
  }

  return (
    <View style={styles.container}>
      <View style={styles.logoContainer}>
        <Text style={styles.rupee}>Rupee</Text>
        <Text style={styles.genie}>Genie</Text>
      </View>
      <View style={styles.iconContainer}>
        <TouchableOpacity onPress={() => alert('Call clicked')}>
          <MaterialIcons name="phone" size={38} color="#0B549D" />
        </TouchableOpacity>
        <TouchableOpacity onPress={() => alert('Notification clicked')}>
          <FontAwesome5 name="bell" size={38} color="#0B549D" />
        </TouchableOpacity>
        <TouchableOpacity onPress={() => alert('Profile clicked')}>
          <FontAwesome5 name="user-circle" size={38} color="#0B549D" />
        </TouchableOpacity>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: 10,
    borderBottomWidth: 3,
    borderBottomColor: '#ccc',
  },
  logoContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  rupee: {
    fontFamily: 'Jomhuria_400Regular',
    fontSize: 38,
    color: '#0B549D',
  },
  genie: {
    fontFamily: 'JollyLodger_400Regular',
    fontSize: 38,
    color: 'orange',
  },
  iconContainer: {
    flexDirection: 'row',
    justifyContent: 'space-evenly',
    width: 230, // Adjust based on icon spacing
  },
});

export default HeaderComponent;
