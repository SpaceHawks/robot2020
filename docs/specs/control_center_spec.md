# Robot Control Center Web Frontend
- In the actual competition, we need to be able to control the robot over the network using only sensors data and we're penalized for bandwidth

## Communication with Robot
- Because communication can have high frequency and involves realtime data, it makes sense to use websockets
- Using a REST API is possible, but will result in higher bandwidth use and higher latency
- JavaScript:
  - client: https://www.tutorialspoint.com/html5/html5_websocket.htm, https://developer.mozilla.org/en-US/docs/Web/API/WebSocket
  - server: https://www.npmjs.com/package/nodejs-websocket
- Python: needs googling

## Architecture
- apart from the xbox controller, all the client functionality can be within a static HTML+CSS+JS page running browser
- we will need a node.js application to give us the hardware access we need to use the xbox controller (xboxdrv) 
- robot will need a websocket daemon which might be difficult to make work with the rest of the robot
- rn I think it makes the most sense to have the robot host the ws server, but subject to change

## Desired Functionality
### Map
Show a map of the arena with all the available data. Items listed in terms of importance.
#### Data visualization for: 
- View detected obstacles
- View robot position
- View planned path
- include data from kalman filter in position datapoint
- Toggle Depth/Height heatmap
- mined areas
- terrain
- historic pathing

### Mode of Operation
Need some buttons to tell robot what to do
- begin autonomous/manual/etc.
- manual override
- emergency stop

### Variables
- View important variables/values/sensor readings
- Adjust coefficients (maybe w/ a slider) so we can quickly tune pid, kalman, etc.

### Debugging & Bandwidth
- verbosity control: reduce bandwith unless we need to debug
- update frequency adjustments: reduce bandwidth by lowering FPS
- console: receive debug messages from the robot

### Logging
- On frontend keep data in memory and have a button to export to log file
- Eventually we can make a logfile viewer
  - or just make a program to play it back
- alternatively it could be saved on the robot

- Save/Download: https://stackoverflow.com/questions/3665115/how-to-create-a-file-in-memory-for-user-to-download-but-not-through-server
- Load/Read: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API

### Data Visualizations
This may not be needed for MVP but I can use d3.js for graphs and other data visualizations
- would likely be needed for logfile viewer

### Communication protocol/Instructions
|Name|Data|Example|
|-------------|----------|-----------|
|Obstacle Point|O:x,y, ...|O:30,23,45,60|
|Robot Point|R:x,y,θ|R:3,2,45|
|Arcade Drive|AD:throttle,turn|AR:85,40|
|Tank Drive|TD:left,right|TD:80,30|
|Autonomous|AI|AI|
|STOP|STOP|STOP|
