import React, { Component } from 'react';

class SubsForm extends Component {


    state = {

    }

    render() {
        return (
        <form>
            <div class="form-group">
              <label for="exampleInputEmail1">Player name</label>
              <input type="text" class="form-control form-border" id="exampleInputEmail1" aria-describedby="emailHelp" placeholder="Enter player name" />
            </div>
            <div class="form-group">
              <label for="exampleInputEmail1">Player's Team</label>
              <input type="text" class="form-control form-border" id="exampleInputEmail1" aria-describedby="emailHelp" placeholder="Enter players club e.g. D2" />
            </div>
            <div class="form-group">
              <label for="exampleInputEmail1">Sub's Paid</label>
              <div class="input-group">
              <div class="input-group-prepend">
                <div class="input-group-text">€</div>
              </div>
              <input type="number" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" placeholder="Subs Paid e.g. €100" />
              </div>
            </div>
            <button type="submit" class="btn btn-primary text-right">Add Subs</button>
        </form>
        )
    }
}

export default SubsForm;