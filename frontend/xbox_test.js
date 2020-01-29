let xbox = require('node-xboxdrv')
let controller = new xbox('045e','0719', {type: 'xbox360-wireless'})

controller.on('leftX', console.log)
