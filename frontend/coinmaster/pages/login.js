import React, { useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet, Alert } from 'react-native';
import { supabase } from '../supabaseee/supacreds';

const Login = ({ navigation }) => {
  const [accountNumber, setAccountNumber] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async () => {
    const { data, error } = await supabase
      .from('users_c')
      .select('*')
      .eq('acc_num', accountNumber)
      .eq('password', password)
      .single();

    if (error || !data) {
      Alert.alert('Login failed', 'Invalid account number or password');
    } else {
      navigation.navigate('Home', { userId: data.id });
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.header}>Login</Text>
      <TextInput
        style={styles.input}
        placeholder="Account Number"
        value={accountNumber}
        onChangeText={setAccountNumber}
      />
      <TextInput
        style={styles.input}
        placeholder="Password"
        secureTextEntry
        value={password}
        onChangeText={setPassword}
      />
      <Button title="Login" onPress={handleLogin} />
      <View style={styles.signupContainer}>
        <Text>Don't have an account?</Text>
        <Button title="Sign Up" onPress={() => navigation.navigate('Signup')} />
      </View>
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
  signupContainer: {
    marginTop: 20,
    alignItems: 'center',
  },
});

export default Login;