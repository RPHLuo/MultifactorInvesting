import React, {Component} from 'react';
import {Platform, StyleSheet, Text, View, TouchableOpacity } from 'react-native';
import Config from "react-native-config";
import Autocomplete from 'react-native-autocomplete-input';
import { ClipPath, Defs } from 'react-native-svg'
import { LineChart, XAxis, YAxis } from 'react-native-svg-charts';
import { ButtonGroup } from 'react-native-elements';

export default class Stock extends Component<Props> {

  state={
    query:'',
    historicalData: [],
    predictData: [],
    data:[],
    availableStocks: [],
    hideSuggestions: true,
    timeIndex: 7,
    buttons: ['5 d', '1 mth', '3 mth', '6 mth', '1 yr', '3 yr', '5 yr', 'max'],
    startDates: [0, 0, 0, 0, 0, 0, 0, 0],
    predictIndex: 0,
    predictButtons: ['None', '20 days', '50 days', '100 days', '200 days'],
    timeStepDays: [0, 20, 50, 100, 200],
    selected: false,
    timeStep: 0,
    dateNumber: 20190531
  }

  constructor(props) {
    super(props)
    this.search = this.search.bind(this)
    this.updateStartTime = this.updateStartTime.bind(this)
    this.updatePredictTime = this.updatePredictTime.bind(this)
    this.updateHistoricalData = this.updateHistoricalData.bind(this)
    this.updatePredictData = this.updatePredictData.bind(this)
  }

  componentDidMount(props) {
    fetch(Config.SERVER+'/available/stocks')
    .then((res)=>res.json()).then(((availableStocks) => { this.setState({availableStocks}) }).bind(this))

    let date = this.formatDate(new Date())
    reduceValues = [5, 100, 300, 600, 10000, 30000, 50000, 100000000]
    startDates = []
    for (v in reduceValues) {
      startDates.push(date - reduceValues[v])
    }
    date = new Date()
    date.setDate( date.getDate() - 5 )
    startDates[0] = this.formatDate(date)
    this.setState({startDates})
  }

  formatDate(date) {
    let month = (date.getMonth() + 1)
    let day = date.getDate()
    let year = date.getFullYear()
    if (month < 10) {
      month = '0' + month
    }
    if (day < 10) {
      day = '0' + day
    }
    return parseInt('' + year + month + day)
  }

  updateHistoricalData(historicalData) {
    let data = []
    data.push(...historicalData, ...this.state.predictData)
    this.setState({historicalData, data, selected:true})
  }

  updatePredictData(predictData) {
    let seqResult = JSON.parse(predictData.seq_result)
    seqResult.forEach((item) => {
      item.predict = parseFloat(item.predict)
    })
    let data = []
    data.push(...this.state.historicalData, ...seqResult)
    this.setState({data, predictData: seqResult, target_result: predictData.target_result, selected:true})
  }

  search(ticker) {
    this.state.ticker = ticker
    this.setState({ query: ticker, hideSuggestions:true })
    this.updateStartTime(this.state.startDates.length-1)
  }

  updateStartTime(timeIndex) {
    this.setState({ timeIndex })
    let body = { ticker: this.state.ticker, start: this.state.startDates[timeIndex] }
    fetch(Config.SERVER+'/quote', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
    }).then((res)=>res.json()).then(this.updateHistoricalData)
  }

  updatePredictTime(predictIndex) {
    this.setState({ predictIndex })
    if (!predictIndex) {
      return
    }
    let body = {
      ticker: this.state.ticker,
      time_step: this.state.timeStepDays[predictIndex],
      dateNumber: this.state.dateNumber
    }
    fetch(Config.SERVER+'/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
    }).then((res)=>res.json()).then(this.updatePredictData)
  }

  const Clips = ({ x, width }) => (
    <Defs key={ 'clips' }>
        <ClipPath id="clip-path-1">
            <Rect x={ '0' } y={ '0' } width={ x(indexToClipFrom) } height={ '100%' }/>
        </ClipPath>
        <ClipPath id={ 'clip-path-2' }>
            <Rect x={ x(200) } y={ '0' } width={ width - x(indexToClipFrom) } height={ '100%' }/>
      </ClipPath>
    </Defs>
  )

  const DashedLine = ({ line }) => (
    <Path
      key={ 'line-1' }
      d={ line }
      stroke={ 'rgb(134, 65, 244)' }
      strokeWidth={ 2 }
      fill={ 'none' }
      strokeDasharray={ [ 4, 4 ] }
      clipPath={ 'url(#clip-path-2)' }
    />
  )

  renderStock() {
    if (this.state.selected) {
      return (
        <View>
          <View style={{flex:1}}>
            <View style={{ height: 200, flexDirection: 'row' }}>
              <YAxis
                data={ this.state.data }
                yAccessor={ value => value.close }
                contentInset={ { bottom: 10, top: 10 } }
                svg={{
                  fill: 'grey',
                  fontSize: 10,
                }}
                numberOfTicks={ 4 }
                formatLabel={ value => `${value}` }
              />
              <LineChart
                style={StyleSheet.absolutefill}
                data={ this.state.data.map((item) => item.predict ? item.predict : 0) }
                svg={{ stroke: 'rgb(222, 0, 10)' }}
                contentInset={{ left: 20, top: 10, bottom: 10 }}
              />
              <LineChart
                style={{ flex: 1, marginLeft: 16 }}
                data={ this.state.data.map((item) => item.close ? item.close : 0) }
                svg={{ stroke: 'rgb(134, 65, 244)' }}
                contentInset={{ left: 20, top: 10, bottom: 10 }}
              />
            </View>
            <XAxis
              style={{ marginHorizontal: 10 }}
              data={ this.state.data }
              formatLabel={ (index) => {
                return this.state.data[index].date
              }}
              contentInset={{ left: 20, right: 10 }}
              numberOfTicks={ 2 }
              svg={{ fontSize: 10, fill: 'black' }}
            />
          </View>
          <ButtonGroup
            onPress={this.updateStartTime}
            selectedIndex={this.state.timeIndex}
            buttons={this.state.buttons}
            containerStyle={{height: 30}}
          />
          <ButtonGroup
            onPress={this.updatePredictTime}
            selectedIndex={this.state.predictIndex}
            buttons={this.state.predictButtons}
            containerStyle={{height: 50}}
          />
        </View>
      )
    }
  }
  render() {
    return (
      <View>
        <View style={{
          flex: 1,
          left: 0,
          position: 'absolute',
          right: 0,
          top: 0,
          zIndex: 1
        }}>
          <Autocomplete
            data={this.state.availableStocks}
            defaultValue={this.state.query}
            onChangeText={(text => {
              let hide = (text == '')
              this.setState({ query: text, hideSuggestions:hide })
            }).bind(this)}
            hideResults={this.state.hideSuggestions}
            renderItem={({ item, i }) => (
              <TouchableOpacity
                key={item}
                onPress={this.search.bind(this,item)}
              >
                <Text>{item}</Text>
              </TouchableOpacity>
            )}
          />
          {this.renderStock()}
        </View>
      </View>
    );
  }
}
