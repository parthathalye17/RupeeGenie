import { StatusBar } from 'expo-status-bar';
import React from 'react';
import { StyleSheet, Text, View } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';


const Stack = createNativeStackNavigator();

import Home from './pages/homePage';
import RecentTransactions from './pages/recent_trans';
import OCR from './pages/OCR';
import FormPage from './pages/FormPage';
import ChatScreen from './pages/ChatScreen';
import QRScannerComponent from './pages/QrScanner';

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="ocr">
        <Stack.Screen
          name="ocr"
          component={OCR}
          options={{ headerShown: false }}
        />
        <Stack.Screen
          name="qrscan"
          component={QRScannerComponent}
          options={{ headerShown: false }}
        />
        <Stack.Screen
          name="Chatbot"
          component={ChatScreen}
          options={{ headerShown: false }}
        />
        <Stack.Screen
          name="FormPage"
          component={FormPage}
          options={{ headerShown: false }}
        />

        <Stack.Screen
          name="Home"
          component={Home}
          options={{ headerShown: false }}
        />
        <Stack.Screen
          name="RecentTransacs"
          component={RecentTransactions}
          options={{ headerShown: false }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
