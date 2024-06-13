import React, { useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet, Modal, TouchableOpacity } from 'react-native';

const CardFormModal = ({ visible, onClose, onSubmit }) => {
  const [cardDetails, setCardDetails] = useState({
    accountNumber: '',
    validThru: '',
    cvv: '',
    holderName: ''
  });

  const handleAddCard = () => {
    onSubmit(cardDetails);
    setCardDetails({
      accountNumber: '',
      validThru: '',
      cvv: '',
      holderName: ''
    });
  };

  return (
    <Modal
      animationType="slide"
      transparent={true}
      visible={visible}
      // onRequestClose={!visible}
    >
      <View style={styles.modalContainer}>
        <View style={styles.modalContent}>
          <Text style={styles.modalTitle}>Add Card Details</Text>
          <TextInput
            style={styles.input}
            placeholder="Account Number"
            value={cardDetails.accountNumber}
            onChangeText={(text) => setCardDetails({ ...cardDetails, accountNumber: text })}
          />
          <TextInput
            style={styles.input}
            placeholder="Valid Thru"
            value={cardDetails.validThru}
            onChangeText={(text) => setCardDetails({ ...cardDetails, validThru: text })}
          />
          <TextInput
            style={styles.input}
            placeholder="CVV"
            value={cardDetails.cvv}
            onChangeText={(text) => setCardDetails({ ...cardDetails, cvv: text })}
          />
          <TextInput
            style={styles.input}
            placeholder="Card Holder Name"
            value={cardDetails.holderName}
            onChangeText={(text) => setCardDetails({ ...cardDetails, holderName: text })}
          />
          <View style={styles.buttons}>
            <TouchableOpacity onPress={handleAddCard} style={styles.modalBtn}>
              <Text style={styles.add_card}>Add Card</Text>
            </TouchableOpacity>
            <TouchableOpacity onPress={onClose} style={styles.modalBtnCan}>
              <Text style={styles.add_card}>Cancel</Text>
            </TouchableOpacity>
          </View>
        </View>
      </View>
    </Modal>
  );
};

const styles = StyleSheet.create({
  modalContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'rgba(0,0,0,0.5)',
  },
  modalContent: {
    width: 300,
    padding: 20,
    backgroundColor: '#fff',
    borderRadius: 10,
  },
  modalTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  input: {
    height: 40,
    borderColor: 'gray',
    borderWidth: 1,
    marginBottom: 10,
    paddingHorizontal: 10,
    borderRadius:10,
  },
  but:{
    borderRadius:20,
  },
  buttons: {
    flexDirection: 'row', 
    justifyContent: 'space-evenly'
    
  },
  add_card: {
    color: '#fff',
    marginHorizontal: 10,
    marginVertical: 10
  },
  modalBtn: {
    backgroundColor: '#003D7A',
    borderRadius:10,
  },
  modalBtnCan: {
    backgroundColor: '#B70000',
    borderRadius:10,
  }
});

export default CardFormModal;
