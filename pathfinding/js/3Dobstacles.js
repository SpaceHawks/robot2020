function generateObstacles() {

    /*
        THIS PART JUST RANDOMLY GENERATES OBSTACLES
    */
    let dist = (x1, y1, x2, y2) => Math.sqrt(Math.pow(x2-x1,2) + Math.pow(y2-y1,2));
    let random = (l, h) => Math.random() * (h - l) + l;

    let numObstacles = 5;
    let b = 2;
    let robot = { w: 50, h: 100 };
    let start = {
        x: Math.round(random(15, 60)),
        y: 90
    };
    let end = {
        x: 36,
        y: 1
    };

    let width = 360;
    let height = 540;
    let obstacles = [];
    let centers = [];
    for (let i = 0; i < numObstacles; i++) {
        let dimensions = null;
        while (!dimensions) {
            let x = random(30, width - 30);
            let y = random(0.33 * height, 0.67 * height);
            let r = random(30, 50) / 2;

            if (centers.some(c => dist(c.x, c.y, x, y) < r + c.r)) {
                continue;
            } else {
                dimensions = { x, y, r };
                centers.push(dimensions);
            }
        }

        let { x, y, r } = dimensions;
        for (let a = 0; a < 2 * Math.PI; a += 0.6) {
            let px = x + r * Math.cos(a) + random(-0.3, 7);
            let py = y + r * Math.sin(a) + random(-0.3, 7);
            obstacles.push({
                x: px,
                y: py,
                d: 3,
                hidden: false
            });
        }
    }


    /*
        ACTUAL TO 3D PART
    */

    let obs = [];

    // Create an empty 3D grid
    for (let x = 0; x <= 72; x++) {
        if (!obs[x]) obs[x] = [];
        for (let y = 0; y <= 108; y++) {
            if (!obs[x][y]) obs[x][y] = [];
            for (let a = 0; a < 180; a += 15) {
                obs[x][y][a] = false;
            }
        }
    }
    let r = {w: 50, h: 100};
    for (let o of obstacles) {
        for (let a = 0; a < 180; a += 15) {
            // Check square area around obstacle to see which points collide at angle
            for (let dx = -100; dx < 100; dx+=5) {
                for (let dy = -100; dy < 100; dy+=5) {
                    // Determine if point intersects rotated robot
                    if (pointInRobot({x: o.x + dx, y: o.y + dy}, {x: o.x, y: o.y, a: a - 75, w: robot.w, h: robot.h})) {
                        try { // just in case o.x + dx goes out of bounds
                            obs[Math.round((o.x+dx)/5)][Math.round((o.y+dy)/5)][a] = true;
                        } catch(e) {}
                    }
                }
            }
        }
    }

    return obs;
}

/*
    Helper function that uses the rotation matrix to check if an obstacle is
    inside of the rotated robot
*/
function pointInRobot(_o, r) {
    if (!r) r = robot;
    // Set origin of point to robot center
    let oP = {x: _o.x - r.x, y: _o.y - r.y};
    // Rotation angle
    _a = -r.a * Math.PI / 180;
    // Rotate angle
    let P = {
      x: oP.x*Math.cos(_a) - oP.y*Math.sin(_a),
      y: oP.x*Math.sin(_a) + oP.y*Math.cos(_a)
    };
    let insideX = P.x > -r.w / 2 && P.x < r.w / 2;
    let insideY = P.y > -r.h / 2 && P.y < r.h / 2;
    return (insideX && insideY)
}

let start = Date.now();
generateObstacles();
console.log((Date.now() - start) / 1000);

module.exports = generateObstacles;
