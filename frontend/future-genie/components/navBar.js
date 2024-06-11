// BottomNavBar.js
import React from 'react';
import { View, TouchableOpacity, StyleSheet } from 'react-native';
import Icon from 'react-native-vector-icons/Ionicons';
import { useNavigation } from '@react-navigation/native';

const BottomNavBar = () => {
  const navigation = useNavigation();

//   const handleQr = async () => {
//     navigation.navigate{'QRpage'}

//   }

  return (
    <View style={styles.container}>
      <TouchableOpacity style={styles.iconContainer} onPress={() => console.log('home')}>
        <Icon name="home-outline" size={30} color="#fff" />
      </TouchableOpacity>
      <TouchableOpacity style={styles.iconContainer} onPress={() => console.log('Chat pressed')}>
        <Icon name="chatbubble-outline" size={30} color="#fff" />
      </TouchableOpacity>
      <TouchableOpacity style={styles.iconContainer} onPress={() => console.log('QR pressed')}>
        <Icon name="qr-code-outline" size={30} color="#fff" />
      </TouchableOpacity>
      <TouchableOpacity style={styles.iconContainer} onPress={() => console.log('Card pressed')}>
        <Icon name="card-outline" size={30} color="#fff" />
      </TouchableOpacity>
      <TouchableOpacity style={styles.iconContainer} onPress={() => console.log('Profile pressed')}>
        <Icon name="person-outline" size={30} color="#fff" />
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    backgroundColor: '#0B549D',
    paddingVertical: 20,
    paddingBottom: 20,
  },
  iconContainer: {
    alignItems: 'center',
    borderColor: 'black',
  },
});

export default BottomNavBar;
