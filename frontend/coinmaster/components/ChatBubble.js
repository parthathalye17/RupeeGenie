
// ChatBubble.js
import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

const ChatBubble = ({ message }) => {
  return (
    <View style={message.type === 'user' ? styles.userBubble : styles.botBubble}>
      <Text style={message.type === 'user' ? styles.userText : styles.botText}>
        {message.text}
      </Text>
    </View>
  );
};

const styles = StyleSheet.create({
  userBubble: {
    alignSelf: 'flex-end',
    backgroundColor: '#007bff',
    borderRadius: 15,
    padding: 10,
    marginVertical: 5,
    maxWidth: '80%',
  },
  botBubble: {
    alignSelf: 'flex-start',
    backgroundColor: '#e0e0e0',
    borderRadius: 15,
    padding: 10,
    marginVertical: 5,
    maxWidth: '80%',
  },
  userText: {
    color: '#fff',
  },
  botText: {
    color: '#000',
  },
});

export default ChatBubble;
