import React, { useState, useEffect } from 'react';
import { Text, View, StyleSheet, TouchableOpacity } from 'react-native';
import * as SplashScreen from 'expo-splash-screen';
import { useFonts, Jomhuria_400Regular } from '@expo-google-fonts/jomhuria';
import { JollyLodger_400Regular } from '@expo-google-fonts/jolly-lodger';
import { MaterialIcons, FontAwesome5 } from '@expo/vector-icons';
import Icon from 'react-native-vector-icons/Ionicons';
import QRCodeModal from './qrModal';
import { supabase } from '../supabaseee/supacreds';

SplashScreen.preventAutoHideAsync(); // Prevent the splash screen from auto-hiding

const HeaderComponent = ({ userId }) => {
  const [fontsLoaded] = useFonts({
    Jomhuria_400Regular,
    JollyLodger_400Regular,
  });

  const [modalVisible, setModalVisible] = useState(false);
  const [qrImage, setQrImage] = useState('');

  useEffect(() => {
    if (fontsLoaded) {
      SplashScreen.hideAsync(); // Hide the splash screen once fonts are loaded
    }
  }, [fontsLoaded]);

  const fetchQrCode = async () => {
    try {
      if (!userId) {
        console.error('User ID not found');
        return;
      }

      const { data, error } = await supabase
        .from('users_c')
        .select('qr_code')
        .eq('id', userId)
        .single();

      if (error) {
        console.error('Error fetching QR code:', error);
        return;
      }

      setQrImage(data.qr_code);
      setModalVisible(true);
    } catch (error) {
      console.error('Unexpected error fetching QR code:', error);
    }
  };

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
        <TouchableOpacity onPress={fetchQrCode}>
          <Icon name="qr-code-outline" size={38} color="#0B549D" />
        </TouchableOpacity>
        <TouchableOpacity onPress={() => alert('Notification clicked')}>
          <FontAwesome5 name="bell" size={38} color="#0B549D" />
        </TouchableOpacity>
        <TouchableOpacity onPress={() => alert('Profile clicked')}>
          <FontAwesome5 name="user-circle" size={38} color="#0B549D" />
        </TouchableOpacity>
      </View>
      <QRCodeModal
        modalVisible={modalVisible}
        setModalVisible={setModalVisible}
        qrImage={qrImage}
      />
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
