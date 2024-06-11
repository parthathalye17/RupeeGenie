// BottomNavBar.js
import React from 'react';
import { View, TouchableOpacity, StyleSheet , Text , Image } from 'react-native';
import Icon from 'react-native-vector-icons/Ionicons';
import { useNavigation } from '@react-navigation/native';

const Invest = () => {

    return(
        <View style={styles.box}>
        <Text style={styles.title}>Investments</Text>
            <View style={styles.investmentContainer}>
                <TouchableOpacity style={styles.investmentItem}>
                <Image source={require('../assets/crypto.png')} style={styles.icon} />
                <Text style={styles.label}>crypto</Text>
                </TouchableOpacity>
                <TouchableOpacity style={styles.investmentItem}>
                <Image source={require('../assets/stocks.png')} style={styles.icon} />
                <Text style={styles.label}>stocks</Text>
                </TouchableOpacity>
                <TouchableOpacity style={styles.investmentItem}>
                <Image source={require('../assets/bonds.png')} style={styles.icon} />
                <Text style={styles.label}>bonds</Text>
                </TouchableOpacity>
            </View>


        </View>

    );

}

const styles = StyleSheet.create({
    box: {

    },
    title: {
        fontSize: 24,
        fontWeight: 'bold',
        marginBottom: 6,
      },
      investmentContainer: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        padding: 15,
        borderWidth: 2,
        borderColor: '#000',
        borderRadius: 10,
        width: '50%',
        
        
      },
      investmentItem: {
        alignItems: 'center',
        flex: 1,
        
      },
      icon: {
        width: 30,
        height: 30,
        marginBottom: 5,
        
      },
      label: {
        fontSize: 16,
      },



});

export default Invest;