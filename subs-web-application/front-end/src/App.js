import React, { Component, Fragment } from 'react';
import SubsForm from './SubsForm';
import './App.css';

class App extends Component {
  render() {
    return (
      <Fragment>
        <h1>DL Subs Tracker</h1>
        <SubsForm />
      </Fragment>
    );
  }
}

export default App;
