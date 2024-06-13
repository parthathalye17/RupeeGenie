import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, TouchableOpacity, View, ScrollView } from 'react-native';
import { React, useState, useEffect } from 'react';
import { SafeAreaView } from 'react-native-safe-area-context';

import BottomNavBar from '../components/navBar';
import RecentTrans from '../components/transactions';
import PaymentOptions from '../components/pay';
import Invests from '../components/investments';
import HeaderComponent from '../components/header';
import CardCarousel from '../components/carousel';
import Documents from '../components/docs';

export default function Home({ navigation }) {
  return (
    <>
     
      <SafeAreaView style={styles.container}>
        <HeaderComponent/>
        <ScrollView contentContainerStyle={styles.scrollContainer}>
          <CardCarousel />
          <RecentTrans navigation={navigation} />
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
    // backgroundColor: "#fff"
  },
  scrollContainer: {
    flexGrow: 1,
    paddingBottom: 20, // Add some padding at the bottom for better spacing
  },
  nav: {},
});
