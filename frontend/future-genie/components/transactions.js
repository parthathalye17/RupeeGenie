import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import LinearGradient from 'react-native-linear-gradient';

const RecentTrans = () => {
  return (
    <View style={styles.container}>
        
      {/* <Text style={styles.title}>Recent transactions</Text> */}
      {/* <LinearGradient style={styles.groupChild} locations={[0,1]} colors={['#0b549d','#002244']} useAngle={true} angle={103.63} /> */}
      <View style={styles.card}>
        <Text style={styles.label}>Account Type</Text>
        <Text style={styles.accountNumber}>1234 5678 1234</Text>
        <Text style={styles.balanceLabel}>Available Balance</Text>
        <Text style={styles.balance}>$ XXX, XXX. XX</Text>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    padding: 20,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 6,
  },
  card: {
    backgroundColor: '#1C1C2E', // dark background color
    borderRadius: 15,
    padding: 20,
    // position: "absolute"
  },
  label: {
    color: '#FFFFFF',
    fontSize: 14,
    marginBottom: 5,
  },
  accountNumber: {
    color: '#FFFFFF',
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
  },
  balanceLabel: {
    color: '#C0C0C0',
    fontSize: 14,
    marginBottom: 5,
  },
  balance: {
    color: '#FFFFFF',
    fontSize: 24,
    fontWeight: 'bold',
  },
});

export default RecentTrans;