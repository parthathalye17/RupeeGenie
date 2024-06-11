
import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import { React, useState, useEffect } from 'react';



import BottomNavBar from '../components/navBar';
import Invest from '../components/investments';
import RecentTrans from '../components/transactions';

export default function Home() {



  return (
    <>
      <View style = {styles.container}> 

      </View>
      <RecentTrans/>
      <Invest/>
      

     

      <BottomNavBar style = {styles.nav}/>
    </>
  );
}

const styles = StyleSheet.create({
  container: {
  
    flex: 1,
    

  },

  nav: {
    
    
  }
});

