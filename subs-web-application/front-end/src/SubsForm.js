import React, { Component } from 'react';

class SubsForm extends Component {


    state = {
        name: '',
        team: '',
        paid: 0,
    }

    onSubmit = async (e) => {
        e.preventDefault();
    
        const { name, team, paid } = this.state;
        const newEntry = {
          name,
          team,
          paid,
        };

        console.log(newEntry)
    }

    handleInputChange = (e) => {
        const { name, value } = e.target;
        this.setState({ [name]: value });
    }

    render() {
        return (
        <form onSubmit={this.onSubmit}>
            <div className="form-group">
              <label htmlFor="inputName">Player name</label>
              <input type="text" className="form-control form-border" id="inputName" name="name" placeholder="Enter player name" value={this.state.name} onChange={this.handleInputChange} />
            </div>
            <div className="form-group">
              <label htmlFor="inputTeam">Player's Team</label>
              <input type="text" className="form-control form-border" id="inputTeam" name="team" placeholder="Enter players club e.g. D2" value={this.state.team} onChange={this.handleInputChange} />
            </div>
            <div className="form-group">
              <label htmlFor="inputPaid">Sub's Paid</label>
              <div className="input-group">
              <div className="input-group-prepend">
                <div className="input-group-text">€</div>
              </div>
              <input type="number" className="form-control" id="inputPaid" name="paid" placeholder="100" value={this.state.paid} onChange={this.handleInputChange} />
              </div>
            </div>
            <button type="submit" className="btn btn-primary text-right">Add Subs</button>
        </form>
        )
    }
}

export default SubsForm;