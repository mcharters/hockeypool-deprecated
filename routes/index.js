
/*
 * GET home page.
 */

exports.index = function(req, res){
  res.render('index', { title: 'hockeypool' });
};

exports.admin = function(req, res){
  res.render('admin', { title: 'Express' });
};