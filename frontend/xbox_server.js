const express = require('express')
const app = express()
const port = 3000

let xbox = require('node-xboxdrv')
let controller = new xbox('045e','0719', 'xbox360-wireless')

app.get('/spacehawks-xbox', (req, res) => res.send("Server is Running"))

app.get('/leftX', (req, res) => {
    controller.on('leftX', data => res.json(100 * data / 32768))
})

app.get('/leftY', (req, res) => {
    controller.on('leftY', data => res.json(100 * data / 32768))
})

app.get('/rightX', (req, res) => {
    controller.on('rightX', data => res.json(100 * data / 32768))
})

app.get('/rightY', (req, res) => {
    controller.on('rightY', data => res.json(100 * data / 32768))
})

app.listen(port)
