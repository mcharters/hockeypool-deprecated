import 'babel-polyfill';
import React from 'react';
import ReactDOM from 'react-dom';

const rootEl = document.getElementById('root');

let render = () => {
  const App = require('./components/App').default;
  ReactDOM.render(
    <App />,
    rootEl
  );
};

if (module.hot) {
  const renderApp = render;
  const renderError = (error) => {
    const RedBox = require('redbox-react');
    render(
      <RedBox error={error} />,
      rootEl
    );
  };

  render = () => {
    try {
      renderApp();
    } catch (error) {
      renderError();
    }
  };

  module.hot.accept('./components/App', () => {
    setTimeout(render);
  });
}

render();
