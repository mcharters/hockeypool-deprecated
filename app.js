
/**
 * Module dependencies.
 */

var express = require('express')
  , routes = require('./routes')
  , players = require('./routes/players')
  , teams = require('./routes/teams')
  , http = require('http')
  , path = require('path');

/**
 * DB dependencies.
 */
var mongo = require('mongodb')
  , mongoServer = new mongo.Server('localhost', 27017, {auto_reconnect: true})
  , mongodb = new mongo.Db('hockeypool', mongoServer);


var app = express();

// all environments
app.set('port', process.env.PORT || 3000);
app.set('views', __dirname + '/views');
app.set('view engine', 'ejs');

// db connection
app.use(function(req, res, next) {
	req.mongodb = mongodb;
	next();
});

app.use(express.favicon());
app.use(express.logger('dev'));
app.use(express.bodyParser());
app.use(express.methodOverride());
  app.use(express.cookieParser('your secret here'));
  app.use(express.session());
app.use(app.router);
  app.use(require('stylus').middleware(__dirname + '/public'));
app.use(express.static(path.join(__dirname, 'public')));

// development only
if ('development' == app.get('env')) {
  app.use(express.errorHandler());
}

app.get('/', routes.index);
app.get('/players', players.findAll);
app.get('/teams', teams.findAll);

http.createServer(app).listen(app.get('port'), function(){
	console.log('Express server listening on port ' + app.get('port'));
});
