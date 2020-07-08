import React, {Component} from 'react';
import TextField from '@material-ui/core/TextField';
import ReactList from 'react-list';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';

import logo from './logo.svg';
import './App.css';
import * as requests from "./requests";

class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
            search_text: '',
            search_text_submitted: '',
        };
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleChange(event) {
        this.setState({search_text: event.target.value});
    }

    handleSubmit(event) {
        event.preventDefault();
        this.setState(state => {
            return {...state, search_text_submitted: state.search_text}
        });
    }

    render() {
        return (
            <div>
                <form
                    onSubmit={this.handleSubmit}
                >
                    <TextField
                        id="search"
                        label="Поиск"
                        type="search"
                        onChange={this.handleChange}
                        value={this.state.search_text}
                    />
                </form>
                <EntityList
                    // search_text for searching on-fly, search_text_submitted after hitting Enter
                    search_text={this.state.search_text}
                />
            </div>
        );
    }
}


class EntityList extends Component {
    constructor(props) {
        super(props);

        this.state = {
            authors: [],
        };
    }

    componentDidUpdate(prevProps) {
        const search_text = this.props.search_text;
        if (search_text && search_text !== prevProps.search_text) {
            requests.get('search/authors?text=' + search_text)
                .then(json => this.setState({authors: json}));
        }
    }

    renderItem(index, key) {
        const author = this.state.authors[index];
        return <ListItem key={key}>
            {author.first_name} {author.middle_name} {author.last_name}
        </ListItem>;
    }

    render() {
        return (
            <List>
                <ReactList
                    itemRenderer={(index, key) => this.renderItem(index, key)}
                    //itemsRenderer={}
                    length={this.state.authors.length}
                    type='uniform'
                />
            </List>
        );
    }
}

export default App;
