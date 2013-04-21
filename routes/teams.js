exports.findAll = function(req, res) {
	req.mongodb.collection('teams', function(err, collection) {
		collection.find().toArray(function(err, items) {
			res.send({
				status: "success",
				data: {
					"teams": items
				}
			});
		});
	});
}