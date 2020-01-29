const express = require('express')
const app = express()
const port = 3000

let xbox = require('node-xboxdrv')
let controller = new xbox('045e','0719', 'xbox360-wireless')

app.get('/spacehawks-xbox', (req, res) => res.send("Server is Running"))

app.get('/leftX', (req, res) => {
  controller.on('leftX', data => res.json(data/32768))
})

app.get('/leftY', (req, res) => {
  controller.on('leftY', res.json)
})

app.get('/rightX', (req, res) => {
  controller.on('rightX', res.json)
})

app.get('/rightY', (req, res) => {
  controller.on('rightY', res.json)
})

app.listen(port)
