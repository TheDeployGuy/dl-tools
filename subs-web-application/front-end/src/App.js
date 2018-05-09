import React from 'react';
import SubsForm from './SubsForm';
import Navbar from './Navbar'
import './App.css';

class App extends React.Component {
  render() {
    return (
      <React.Fragment>
        <Navbar />
        <SubsForm />
      </React.Fragment>
    );
  }
}

export default App;
