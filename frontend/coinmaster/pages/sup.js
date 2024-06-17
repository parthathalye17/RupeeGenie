import React, { useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet, Alert } from 'react-native';
import { supabase } from '../supabaseee/supacreds';
import QRCode from 'qrcode';

const generateQRCode = async (data) => {
  try {
    const qrCodeOptions = {
      errorCorrectionLevel: 'L', // Low error correction level to make QR code smaller
      type: 'image/png',
      quality: 0.8,
      margin: 1,
      width: 256 // Adjust width for smaller QR code
    };

    const qrCodeUrl = await QRCode.toDataURL(data, qrCodeOptions);
    return qrCodeUrl;
  } catch (error) {
    console.error('Error generating QR code:', error);
    throw error;
  }
};

const Signup = ({ navigation }) => {
  const [accountNumber, setAccountNumber] = useState('');
  const [upiId, setUpiId] = useState('');
  const [name, setName] = useState('');
  const [password, setPassword] = useState('');
  const [balance, setBalance] = useState(0);

  const handleSignup = async () => {
    try {
      console.log('Starting signup process');

      const qrCodeData = `acc_num:${accountNumber}`;
      const qrCodeUrl = await generateQRCode(qrCodeData);

      console.log('QR code generated:', qrCodeUrl);

      const { data, error } = await supabase
        .from('users_c')
        .insert([{ acc_num: accountNumber, upi_id: upiId, name, password, balance, qr_code: qrCodeUrl }])
        .select();

      if (error) {
        console.error('Signup failed:', error);
        Alert.alert('Signup failed', error.message);
        return;
      }

      console.log('User inserted:', data);
      Alert.alert('Signup successful', 'Please login to continue');
      navigation.navigate('Login');
    } catch (error) {
      console.error('Unexpected error during signup:', error);
      Alert.alert('Unexpected error during signup', error.message);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.header}>Signup</Text>
      <TextInput
        style={styles.input}
        placeholder="Account Number"
        value={accountNumber}
        onChangeText={setAccountNumber}
      />
      <TextInput
        style={styles.input}
        placeholder="UPI ID"
        value={upiId}
        onChangeText={setUpiId}
      />
      <TextInput
        style={styles.input}
        placeholder="Name"
        value={name}
        onChangeText={setName}
      />
      <TextInput
        style={styles.input}
        placeholder="Password"
        secureTextEntry
        value={password}
        onChangeText={setPassword}
      />
      <TextInput
        style={styles.input}
        placeholder="Balance"
        keyboardType="numeric"
        value={balance.toString()}
        onChangeText={text => setBalance(Number(text))}
      />
      <Button title="Signup" onPress={handleSignup} />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    padding: 20,
  },
  header: {
    fontSize: 24,
    marginBottom: 20,
    textAlign: 'center',
  },
  input: {
    height: 40,
    borderColor: 'gray',
    borderWidth: 1,
    marginBottom: 20,
    padding: 10,
  },
});

export default Signup;
