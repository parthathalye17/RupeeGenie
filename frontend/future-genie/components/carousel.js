import React, { useState } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Dimensions, FlatList } from 'react-native';
import CardFormModal from './CardFormModal';

const { width } = Dimensions.get('window');
const cardWidth = width - 40;

const CardCarousel = () => {
  const [cards, setCards] = useState([]);
  const [modalVisible, setModalVisible] = useState(false);

  const handleAddCard = (newCard) => {
    setCards([...cards, { ...newCard, id: cards.length + 1, title: `Card ${cards.length + 1}` }]);
    setModalVisible(false);
  };

  const renderItem = ({ item }) => (
    <View style={item.id === 'add-card' ? styles.addCard : styles.card}>
      {item.id === 'add-card' ? (
        <TouchableOpacity style={styles.addCardContent} onPress={() => setModalVisible(true)}>
          <Text style={styles.addCardText}>Add Card</Text>
        </TouchableOpacity>
      ) : (
        <>
          <Text style={styles.cardTitle}>{item.title}</Text>
          <Text style={styles.cardLabel}>Account Number</Text>
          <Text style={styles.cardNumber}>{item.accountNumber}</Text>
          <View style={styles.cardBottom}>
            <View style={styles.cardHolderContainer}>
              <Text style={styles.cardLabel}>Card Holder</Text>
              <Text style={styles.cardDetail}>{item.holderName}</Text>
            </View>
            <View style={styles.validThruContainer}>
              <Text style={styles.cardLabel}>Valid Thru</Text>
              <Text style={styles.cardDetail}>{item.validThru}</Text>
            </View>
            <View style={styles.cvvContainer}>
              <Text style={styles.cardLabel}>CVV</Text>
              <Text style={styles.cardDetail}>{item.cvv}</Text>
            </View>
          </View>
        </>
      )}
    </View>
  );

  return (
    <View style={styles.container}>
      <FlatList
        data={[...cards, { id: 'add-card', content: 'Add Card' }]}
        horizontal
        pagingEnabled
        showsHorizontalScrollIndicator={false}
        snapToInterval={cardWidth + 20}
        decelerationRate="fast"
        contentContainerStyle={{ paddingHorizontal: 10 }}
        keyExtractor={(item) => item.id.toString()}
        renderItem={renderItem}
      />
      <CardFormModal
        visible={modalVisible}
        onClose={() => setModalVisible(false)}
        onSubmit={handleAddCard}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  card: {
    width: cardWidth,
    height: 300,
    backgroundColor: '#1e1e1e',
    borderRadius: 10,
    marginHorizontal: 10,
    padding: 20,
    justifyContent: 'space-between',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.8,
    shadowRadius: 2,
    elevation: 5,
  },
  addCard: {
    width: cardWidth,
    height: 300,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#007bff',
    borderRadius: 10,
    marginHorizontal: 10,
    padding: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.8,
    shadowRadius: 2,
    elevation: 5,
  },
  addCardContent: {
    justifyContent: 'center',
    alignItems: 'center',
  },
  cardTitle: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  cardLabel: {
    color: '#fff',
    fontSize: 10,
    textTransform: 'uppercase',
  },
  cardNumber: {
    color: '#fff',
    fontSize: 20,
    letterSpacing: 3,
    textAlign: 'left',
    marginBottom: 50,
  },
  cardBottom: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    marginBottom: 20,
  },
  cardHolderContainer: {
    flex: 1,
  },
  validThruContainer: {
    flex: 1,
    alignItems: 'center',
  },
  cvvContainer: {
    flex: 1,
    alignItems: 'flex-end',
    marginRight: 20,
  },
  cardDetail: {
    color: '#fff',
    fontSize: 14,
    marginTop: 5,
  },
  addCardText: {
    color: '#fff',
    fontWeight: 'bold',
    fontSize: 18,
  },
});

export default CardCarousel;