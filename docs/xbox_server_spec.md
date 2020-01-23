# Control Center Server
The only reason we need this is because the control center webpage cannot have direct access to the hardware


# Libraries
## Xbox Controller API
- Use: [node-xboxdrv](https://www.npmjs.com/package/node-xboxdrv) (IMO best)
  - reasonable featureset
  - just a wrapper for xboxdrv
  
- Fallback: [xbox-controller-node](https://www.npmjs.com/package/xbox-controller-node)
  - more features
  - more dependencies (harder setup+installation)
  - slightly more recent
  - some excess features
 
## API Server
use [Express.js](https://expressjs.com/)



# API Planning
- API endpoints that give current position of joysticks
- We'll deal with buttons later :)
