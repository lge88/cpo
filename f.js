
function myFun(x1, x2) {
  return x1*x1 + x2*x2;
}

//
var rl = require('readline').createInterface({
  input: process.stdin,
  output: process.stdout
});

var params = [];

rl.on('line', function(line) {
  var x = parseFloat(line);
  params.push(x);
});

process.on('exit', function() {
  var y = myFun(params[0], params[1])
  console.log(y);
});
