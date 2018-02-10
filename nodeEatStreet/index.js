var handler = function(req, res) {
    fs.readFile('./page.html', function (err, data) {
        if(err) throw err;
        res.writeHead(200);
        res.end(data);
    });
};

var initFunc = function() {
    var es = document.createElement('script'); es.type = 'text/javascript'; es.async = true;
    es.src = ('https:' == document.location.protocol ? 'https://' : 'http://developers.') + 'eatstreet.com/api-js-sdk/js/sdk-remote.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(es, s);
};


var app = require('http').createServer(handler);
var io = require('socket.io').listen(app);
var fs = require('fs');
var csv = require('fast-csv');
var Moniker = require('moniker');
var port = 3250;
var myval = 0;
var commis = 1.0;
var spread = 0.01;



console.log("Parsing...");


app.listen(port);

initFunc();

ESApi.init('308c457ee6398852');


ESApi.searchRestaurants({ 'street-address': '316 W. Washington Ave. Madison, WI' }, function(response) {
    var address = response.address;
    var restaurants = response.restaurants;
    console.log(address, restaurants);
});









