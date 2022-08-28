  // object of express
const express = require('express');
const app = express();
const bodyParser = require('body-parser');
// const message_style = process.env.MESSAGE_STYLE ;

app.use("/public", express.static(__dirname + "/public"));

  // middle ware function works on a global path 
  // but can be designed to work only on a set path
app.use(function(req,res,next){
  console.log(`${req.method} ${req.path} - ${req.ip}`);
  next();
});

  // body parser
app.use(bodyParser.urlencoded({extended: false}));

app.route("/name").get(function(req,res){
  console.log(req.query);
  res.json({name: `${req.query.first} ${req.query.last}`});
}).post(function(req,res){
  console.log(req.body);
  res.json({name: `${req.body.first} ${req.body.last}`});
});

  //middle ware working on a set path -> /now
app.get("/now", function(req,res,next) {
  req.time = (new Date()).toString();
  next();
},
function(req,res){
  res.json({time: req.time});
});


  // route params
app.get("/:word/echo", function(req,res){
  console.log(req.params);
  res.json({echo : req.params.word});
});

//   // route query -> multiple parameters
// app.get("/name", function(req,res){
//   console.log(req.query);
//   res.json({name: `${req.query.first} ${req.query.last}`});
// });

  // get -> go a a particular path and do certain operations 
app.get("/json", function(req,res){

  const initial_Hello_Json = "Hello json";
  let sendMessage;
  if(process.env.MESSAGE_STYLE === 'uppercase')
  {
    sendMessage = initial_Hello_Json.toUpperCase();
  }
  else
  {
    sendMessage = initial_Hello_Json;
  }
  
  const data = {
    "message": sendMessage
  };
  res.json(data);
});

app.get("/", function(req, res) {
  const absolutePath = __dirname + "/views/index.html";
  console.log(absolutePath);
  res.sendFile(absolutePath);
});




































 module.exports = app;
