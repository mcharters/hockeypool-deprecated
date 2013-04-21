/**
 * DB dependencies.
 */
var mongo = require('mongodb')
  , mongoServer = new mongo.Server('localhost', 27017, {auto_reconnect: true})
  , db = new mongo.Db('hockeypool', mongoServer);

exports.findAll = function(req, res) {
	db.collection('players', function(err, collection) {
		collection.find().toArray(function(err, items) {
			res.send({
				status: "success",
				data: {
					"players": items
				}
			});
		});
	});
}