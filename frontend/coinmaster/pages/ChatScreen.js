// ChatScreen.js
import React, { useState } from 'react';
import { View, TextInput, Button, ScrollView, StyleSheet, SafeAreaView } from 'react-native';
import axios from 'axios';
import ChatBubble from '../components/ChatBubble';

const ChatScreen = () => {
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState([]);

  const sendQuery = async () => {
    if (query.trim() === '') return;

    // Add user message to chat
    const userMessage = { text: query, type: 'user' };
    setMessages([...messages, userMessage]);

    // Clear input
    setQuery('');

    try {
      // Send query to backend
      const res = await axios.post('http://192.168.66.58:8000/chatbot/', { question: query });
      const botResponse = { text: res.data.response, type: 'bot' };

      // Add bot response to chat
      setMessages(prevMessages => [...prevMessages, botResponse]);
    } catch (error) {
      console.error(error);
      // Add error message to chat
      const errorMessage = { text: 'Error communicating with chatbot.', type: 'bot' };
      setMessages(prevMessages => [...prevMessages, errorMessage]);
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView style={styles.chatContainer} contentContainerStyle={styles.chatContent}>
        {messages.map((message, index) => (
          <ChatBubble key={index} message={message} />
        ))}
      </ScrollView>
      <View style={styles.inputContainer}>
        <TextInput
          style={styles.input}
          placeholder="Type your message..."
          value={query}
          onChangeText={text => setQuery(text)}
        />
        <Button title="Send" onPress={sendQuery} />
      </View>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  chatContainer: {
    flex: 1,
    padding: 10,
  },
  chatContent: {
    flexGrow: 1,
    justifyContent: 'flex-end',
  },
  inputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 10,
    borderTopWidth: 1,
    borderTopColor: '#ddd',
  },
  input: {
    flex: 1,
    height: 40,
    borderColor: 'gray',
    borderWidth: 1,
    borderRadius: 20,
    paddingHorizontal: 10,
    marginRight: 10,
  },
});

export default ChatScreen;
