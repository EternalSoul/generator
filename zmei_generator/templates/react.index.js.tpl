{{ imports }}

export { {% for page in pages %}{{ page }}{{ "," if not loop.last }}{% endfor %} };
export { {% for page in pages %}{{ page }}Reducer{{ "," if not loop.last }}{% endfor %} };

import './index.scss';

import React from 'react';
import ReactDOM from 'react-dom';
import ReactDOMServer from 'react-dom/server';

import {createStore} from 'redux'
import {Provider} from 'react-redux'

const renderElement = (rootReducer, component, state) => {

    const store = createStore(rootReducer, state);

    store.dispatch({type: 'INIT'});

    return <Provider store={store}>
        {React.createElement(component)}
    </Provider>
};

export const renderClient = (rootReducer, component, state, targetElement) => {
    return ReactDOM.hydrate(renderElement(rootReducer, component, state), targetElement);
};

export const renderServer = (rootReducer, component, state) => {
    return ReactDOMServer.renderToString(renderElement(rootReducer, component, state), null);
};