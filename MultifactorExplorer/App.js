import React, {Component} from 'react';
import {Platform, StyleSheet, Text, View} from 'react-native';
import Stock from './src/Stock'

export default class App extends Component<Props> {
  render() {
    return (
      <View>
        <Stock/>
      </View>
    );
  }
}
