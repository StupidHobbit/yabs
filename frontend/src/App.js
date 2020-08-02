import React, {Component} from 'react';
import TextField from '@material-ui/core/TextField';
import ReactList from 'react-list';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';

import logo from './logo.svg';
import './App.css';
import * as requests from "./requests";
import AppBar from "@material-ui/core/AppBar";
import Tabs from "@material-ui/core/Tabs";
import Typography from "@material-ui/core/Typography";
import Box from "@material-ui/core/Box";
import Tab from "@material-ui/core/Tab";

class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
            search_text: '',
            search_text_submitted: '',
            search_type: 0,
        };
        this.handleChangeText = this.handleChangeText.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleChangeType = this.handleChangeType.bind(this);
    }

    handleChangeText(event) {
        this.setState({search_text: event.target.value});
    }

    handleChangeType(event, value) {
        console.log(value);
        this.setState({search_type: value});
    }

    handleSubmit(event) {
        event.preventDefault();
        this.setState(state => {
            return {...state, search_text_submitted: state.search_text}
        });
    }

    render() {
        const {search_type} = this.state;
        return (
            <div>
                <AppBar position="static">
                    <Tabs value={search_type} onChange={this.handleChangeType} aria-label="search tabs">
                        <Tab label="Авторы" id={0}/>
                        <Tab label="Книги" id={1}/>
                    </Tabs>
                </AppBar>
                <form onSubmit={this.handleSubmit}>
                    <TextField
                        id="search"
                        label="Поиск"
                        type="search"
                        onChange={this.handleChangeText}
                        value={this.state.search_text}
                    />
                </form>
                <TabPanel value={search_type} index={0}>
                    <EntityList
                        // search_text for searching on-fly, search_text_submitted after hitting Enter
                        search_text={this.state.search_text}
                        type='authors'
                        renderEntity={entity => `${entity.first_name} ${entity.middle_name} ${entity.last_name}`}
                    />
                </TabPanel>
                <TabPanel value={search_type} index={1}>
                    <EntityList
                        search_text={this.state.search_text}
                        type='books'
                        renderEntity={entity => `${entity.title}`}
                    />
                </TabPanel>
            </div>
        );
    }
}


function TabPanel(props) {
    const {children, value, index, ...other} = props;

    return (
        <div
            role="tabpanel"
            hidden={value !== index}
            id={`simple-tabpanel-${index}`}
            aria-labelledby={`simple-tab-${index}`}
            {...other}
        >
            {value === index && (
                <Box p={3}>
                    <Typography>{children}</Typography>
                </Box>
            )}
        </div>
    );
}


class EntityList extends Component {
    constructor(props) {
        super(props);

        this.state = {
            entities: [],
        };

        this.componentDidUpdate({});
    }

    componentDidUpdate(prevProps) {
        const search_text = this.props.search_text;
        if (search_text && search_text !== prevProps.search_text) {
            requests.get(`search/${this.props.type}?text=${search_text}`)
                .then(json => this.setState({entities: json}));
        }
    }

    renderItem(index, key) {
        const entity = this.state.entities[index];
        return <ListItem key={key}>
            {this.props.renderEntity(entity)}
        </ListItem>;
    }

    render() {
        return (
            <List>
                <ReactList
                    itemRenderer={(index, key) => this.renderItem(index, key)}
                    length={this.state.entities.length}
                    type='uniform'
                />
            </List>
        );
    }
}

export default App;
