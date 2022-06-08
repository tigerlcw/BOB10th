var express = require('express');
var app = express();

app.get('/', function(req,res){
    res.send('hello express!');

});

app.listen(8000, () =>
    console.log('express 서버 작동중... http://localhost:8000')
);