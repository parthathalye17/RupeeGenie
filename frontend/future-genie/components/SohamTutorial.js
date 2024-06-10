import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import { React, useState, useEffect } from 'react';



export default function Soham() {
  
  const [variable, setVariable] = useState("Main Text")

  const handleMain =  async () => {
    update = "After Updating";
    setVariable(update)
  }

  return (
    <View style={styles.container}>
      <View style={styles.nav_bar}>
        <Text>Nav Item A</Text>
        <Text>Nav Item B</Text>
      </View>
      <Text style={styles.main_text}>{variable}</Text>
      <TouchableOpacity onPress={() => handleMain()} style={styles.button}>
        <Text style={styles.btn_text}>button</Text>
      </TouchableOpacity>
      <StatusBar style="auto" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    // alignItems: 'center',
    // justifyContent: 'center',
    flexDirection: "column",
  },
  nav_bar: {
    flexDirection: "row",
    gap: 20,
    paddingHorizontal: 20,
    backgroundColor: "#efefef",
    paddingTop: 40,
    paddingBottom: 20
  },
  main_text: {
    alignSelf: "center",
    // marginVertical: "auto",
    marginVertical: 40
  },
  button: {
    marginHorizontal: "auto",
    padding: 10,
    backgroundColor: "blue",
    borderRadius: 20
  },
  btn_text: {
    color: "white"
  }
});

