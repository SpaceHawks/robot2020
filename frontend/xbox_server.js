const express = require('express');
const app = express();
const port = 3000;

// Set correct headers so control center can make requests
app.use(function(req, res, next) {
	res.header("Access-Control-Allow-Origin", "*");
	res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
	next();
});

let xbox = require('./node-xboxdrv');
let controller = new xbox('045e', '0719', { type: 'xbox360-wireless' });

let values = { leftX: 0, leftY: 0, rightX: 0, rightY: 0 };

controller.on('leftX', data => {
	values.leftX = (100 * data / 32768)
	console.log(data);
});
controller.on('leftY', data => values.leftY = (100 * data / 32768));
controller.on('rightX', data => values.rightX = (100 * data / 32768));
controller.on('rightY', data => values.rightY = (100 * data / 32768));

app.get('/', (req, res) => res.send(`Server is running!`));

app.get('/leftX', (req, res) => {
    res.json(values.leftX);
})

app.get('/leftY', (req, res) => {
    res.json(values.leftY);
})

app.get('/rightX', (req, res) => {
    res.json(values.rightX);
})

app.get('/rightY', (req, res) => {
  res.json(values.rightY);
})

app.listen(port, () => {
	console.log(`Server is running on port ${port}`)
});
