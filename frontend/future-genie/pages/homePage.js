import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, TouchableOpacity, View, ScrollView } from 'react-native';
import { React, useState, useEffect } from 'react';
import { SafeAreaView } from 'react-native-safe-area-context';

import BottomNavBar from '../components/navBar';
import RecentTrans from '../components/transactions';
import PaymentOptions from '../components/pay';
import CardCarousel from '../components/carousel';
import Invests from '../components/investments';
import Documents from '../components/docs';
import HeaderComponent from '../components/header';


export default function Home() {
  return (
    <>
      <SafeAreaView style={styles.container}>
        <ScrollView contentContainerStyle={styles.scrollContainer}>
          <HeaderComponent/>
          <CardCarousel />
          <RecentTrans />
          <PaymentOptions />
          <Invests />
          <Documents/>
        </ScrollView>
      </SafeAreaView>
      <BottomNavBar style={styles.nav} />
    </>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  scrollContainer: {
    flexGrow: 1,
    paddingBottom: 20, // Add some padding at the bottom for better spacing
  },
  nav: {},
});
