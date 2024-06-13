import React from 'react';
import { View, Text, StyleSheet, FlatList, TouchableOpacity } from 'react-native';
import { MaterialIcons } from '@expo/vector-icons';

import TransactionBox from '../components/transaction_boxx';

const sampleTransactions = [
    { id: 1, name: 'John Doe', accountNum: '12345678', amount: 400, dateTime: '2024-06-12 14:30' },
    { id: 2, name: 'Jane Smith', accountNum: '87654321', amount: 200, dateTime: '2024-06-11 09:15' },
    { id: 3, name: 'Alice Johnson', accountNum: '11223344', amount: 150, dateTime: '2024-06-10 18:45' },
    { id: 4, name: 'Bob Brown', accountNum: '44332211', amount: 300, dateTime: '2024-06-12 12:00' },
    { id: 5, name: 'Charlie Davis', accountNum: '55667788', amount: 250, dateTime: '2024-06-11 16:20' },
    { id: 6, name: 'Diana Evans', accountNum: '99887766', amount: 100, dateTime: '2024-06-10 14:10' },
    { id: 7, name: 'Ethan Foster', accountNum: '66778899', amount: 450, dateTime: '2024-06-09 11:30' },
    { id: 8, name: 'Fiona Green', accountNum: '44556677', amount: 350, dateTime: '2024-06-08 17:00' },
    { id: 9, name: 'George Harris', accountNum: '33445566', amount: 500, dateTime: '2024-06-07 13:45' },
    { id: 10, name: 'Hannah Irving', accountNum: '22334455', amount: 600, dateTime: '2024-06-06 10:20' },
    { id: 11, name: 'Ian Jackson', accountNum: '11224433', amount: 700, dateTime: '2024-06-05 15:50' },
    { id: 12, name: 'Jackie King', accountNum: '99886677', amount: 800, dateTime: '2024-06-04 09:00' },
    { id: 13, name: 'Kevin Lee', accountNum: '88776655', amount: 150, dateTime: '2024-06-03 12:40' },
    { id: 14, name: 'Linda Martin', accountNum: '77665544', amount: 250, dateTime: '2024-06-02 16:30' },
    { id: 15, name: 'Mike Nelson', accountNum: '66554433', amount: 100, dateTime: '2024-06-01 11:15' },
    { id: 16, name: 'Nancy Brien', accountNum: '55443322', amount: 350, dateTime: '2024-05-31 14:00' },
    { id: 17, name: 'Oliver Perez', accountNum: '44332211', amount: 200, dateTime: '2024-05-30 18:45' },
    { id: 18, name: 'Patricia Quinn', accountNum: '33221100', amount: 300, dateTime: '2024-05-29 10:20' },
    { id: 19, name: 'Quincy Roberts', accountNum: '22110099', amount: 400, dateTime: '2024-05-28 13:50' },
    { id: 20, name: 'Rachel Stevens', accountNum: '11009988', amount: 500, dateTime: '2024-05-27 09:00' },
    { id: 21, name: 'Sam Taylor', accountNum: '00998877', amount: 600, dateTime: '2024-05-26 12:30' },
    { id: 22, name: 'Tina Underwood', accountNum: '99887766', amount: 700, dateTime: '2024-05-25 15:00' },
    { id: 23, name: 'Uma Vincent', accountNum: '88776655', amount: 150, dateTime: '2024-05-24 17:45' },
    { id: 24, name: 'Victor White', accountNum: '77665544', amount: 250, dateTime: '2024-05-23 11:30' },
    { id: 25, name: 'Wendy Xie', accountNum: '66554433', amount: 350, dateTime: '2024-05-22 14:20' },
    { id: 26, name: 'Xander Young', accountNum: '55443322', amount: 450, dateTime: '2024-05-21 16:50' },
    { id: 27, name: 'Yara Zane', accountNum: '44332211', amount: 500, dateTime: '2024-05-20 10:10' },
    { id: 28, name: 'Zoe Adams', accountNum: '33221100', amount: 100, dateTime: '2024-05-19 13:40' },
  ];
  

const RecentTransactions = ({ navigation }) => {
  const renderItem = ({ item }) => (
    <TransactionBox 
      person={item.name} 
      accountNum={item.accountNum} 
      amount={item.amount} 
      dateTime={item.dateTime} 
    />
  );

  return (
    <View style={styles.container}>
      <TouchableOpacity style={styles.backButton} onPress={() => navigation.goBack()}>
        <MaterialIcons name="arrow-back" size={24} color="black" />
        <Text style={styles.backText}>Back</Text>
      </TouchableOpacity>
      <Text style={styles.header}>Recent Transactions</Text>
      {sampleTransactions.length === 0 ? (
        <Text>No transactions</Text>
      ) : (
        <FlatList
          data={sampleTransactions}
          renderItem={renderItem}
          keyExtractor={item => item.id.toString()}
        />
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#fff',
  },
  backButton: {
    marginTop:20,
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 20,
  },
  backText: {
    marginLeft: 5,
    fontSize: 16,
  },
  header: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
  },
});

export default RecentTransactions;
