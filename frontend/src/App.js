import React, {Component} from 'react';
import logo from './logo.svg';
import './App.css';
import TextField from '@material-ui/core/TextField';
import * as requests from "./requests";

class App extends Component {
    constructor(props) {
        super(props);
        this.state = {value: ''};
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleChange(event) {
        this.setState({value: event.target.value});
    }
    handleSubmit(event) {
        event.preventDefault();
        requests.get('search/authors?text=' + this.state.value)
            .then(json => console.log(json));
    }

    render() {
        return (
            <form
                onSubmit={this.handleSubmit}

            >
                <TextField
                    id="search"
                    label="Поиск"
                    type="search"
                    onChange={this.handleChange}
                    value={this.state.value}
                />
            </form>
        );
    }
}

export default App;
