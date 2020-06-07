import React, {Component} from 'react';
import logo from './logo.svg';
import './App.css';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import { FormControl } from '@material-ui/core';
import { Search } from '@material-ui/icons';
import * as requests from "./requests";

class App extends Component {
    constructor(props) {
        super(props);
        this.state = {value: ''};
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleChange(event) {    this.setState({value: event.target.value});  }
    handleSubmit(event) {
        requests.get('search/authors?text=' + this.state.value)
            .then(json => console.log(json));
    }

    render() {
        return (
            <form onSubmit={this.handleSubmit}>
                <TextField
                    id="search"
                    label="Поиск"
                    type="search"
                    onChange={this.handleChange}
                />
            </form>
        );
    }
}

export default App;
