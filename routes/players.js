exports.findAll = function(req, res) {
	req.mongodb.collection('players', function(err, collection) {
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