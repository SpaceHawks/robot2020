const ws = require("nodejs-websocket");
const EventEmitter = require("events");


let xbox = require('../node-xboxdrv');
let controller = new xbox('045e', '0719', { type: 'xbox360-wireless', deadzone: 10000 });

let values = { leftX: 0, leftY: 0, rightX: 0, rightY: 0 };

const datalog = new EventEmitter();

controller.on('leftX', data => {
	values.leftX = Math.round(100 * data / 32768);
	datalog.emit('data', `leftX:${values.leftX}`);
});
controller.on('leftY', data => {
	values.leftY = Math.round(100 * data / 32768);
	datalog.emit('data', `leftY:${values.leftY}`);
});
controller.on('rightX', data => {
	values.rightX = Math.round(100 * data / 32768)
	datalog.emit('data', `rightX:${values.rightX}`);
});
controller.on('rightY', data => {
	values.rightY = Math.round(100 * data / 32768)
	datalog.emit('data', `rightY:${values.rightY}`);
});

controller.on('a', data => datalog.emit('data', `a:${data}`));
controller.on('b', data => datalog.emit('data', `b:${data}`));
controller.on('x', data => datalog.emit('data', `x:${data}`));
controller.on('y', data => datalog.emit('data', `y:${data}`));

const ws_server = ws.createServer(conn => {
	console.log("new ws connection");
	datalog.on('data', data => conn.sendText(data));
}).listen(8001);



const express = require('express');
const app = express();
const port = process.env.PORT || 3000;


// Set correct headers so control center can make requests
app.use(function(req, res, next) {
	res.header("Access-Control-Allow-Origin", "*");
	res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
	next();
});

//
app.get('/', (req, res) => res.send(`Server is running!`));
app.get('/leftX', (req, res) => res.json(values.leftX));
app.get('/leftY', (req, res) => res.json(values.leftY));
app.get('/rightX', (req, res) => res.json(values.rightX));
app.get('/rightY', (req, res) => res.json(values.rightY));

app.listen(port, () => console.log(`Server is running on port ${port}`));
