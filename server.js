const http = require('http');
const express = require('express');
const app = express();
const MongoClient = require('mongodb').MongoClient;
const fetch = require('isomorphic-fetch');

// start our db up and get the hockey stats
const teamsURL = 'http://www.nhl.com/stats/rest/grouped/teams/season/teamsummary?cayenneExp=seasonId=20152016%20and%20gameTypeId=2';
const playersURL = 'http://www.nhl.com/stats/rest/grouped/skaters/season/skatersummary?cayenneExp=seasonId=20152016%20and%20gameTypeId=2';

const mongoURL = 'mongodb://localhost:27017/hockeypool';

MongoClient.connect(mongoURL, (err, db) => {
  console.log('Connected to mongo!');

  fetch(teamsURL)
    .then(response => {
      if (response.status >= 400) {
        throw new Error('Bad response from server');
      }
      return response.json();
    }, () => console.log('Teams fetch failed.'))
    .then(json => {
      console.log('Got teams response');
      const teams = db.collection('teams');
      teams.deleteMany({}).then(() => {
        teams.insertMany(json.data);
        console.log('Created teams');
      }, () => console.log('Teams drop failed'));
    }, () => console.log('JSON teams parse failed'));

  fetch(playersURL)
    .then(response => response.json())
    .then(json => {
      console.log('Got players response');
      const players = db.collection('players');
      players.deleteMany({}).then(() => {
        players.insertMany(json.data);
        console.log('Created players');
      });
    });
});

const webpack = require('webpack');
const webpackDevMiddleware = require('webpack-dev-middleware');
const webpackHotMiddleware = require('webpack-hot-middleware');
const config = require('./webpack.config');

const compiler = webpack(config);
app.use(webpackDevMiddleware(compiler, {
  noInfo: true,
  hot: true,
  publicPath: config.output.publicPath,
  historyApiFallback: true,
}));
app.use(webpackHotMiddleware(compiler));

const apiGet = (collection, res) => {
  MongoClient.connect(mongoURL, (err, db) => {
    const coll = db.collection(collection);
    coll.find().toArray().then(docs => {
      res.send({
        [collection]: docs,
      });
    });
  });
};

app.get('/api/players', (req, res) => apiGet('players', res));
app.get('/api/teams', (req, res) => apiGet('teams', res));

app.get(/.*/, function root(req, res) {
  res.sendFile(__dirname + '/index.html');
});

const server = http.createServer(app);
server.listen(process.env.PORT || 3000, function onListen() {
  const address = server.address();
  console.log('Listening on: %j', address);
  console.log(' -> that probably means: http://localhost:%d', address.port);
});
