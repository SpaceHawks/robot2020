const express = require('express');
const app = express();
const port = 3001;

let xbox = require('node-xboxdrv');
let controller = new xbox('045e','0719', {type: 'xbox360-wireless'});

let values = { leftX: 0, leftY: 0, rightX: 0, rightY: 0 };

controller.on('leftX', data => {
  console.log(data);
  values.leftX = (100 * data / 32768);
});

controller.on('leftY', data => values.leftY = (100 * data / 32768));
controller.on('rightX', data => values.rightX = (100 * data / 32768));
controller.on('rightY', data => values.rightY = (100 * data / 32768));

app.get('/spacehawks-xbox', (req, res) => res.send("Server is Running"));

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

app.listen(port);
