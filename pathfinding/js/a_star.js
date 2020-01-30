const PriorityQueue = require("js-priority-queue");

let degreeMap = {
    0: [-3, 1],
    15: [-2, 1],
    30: [-1, 1],
    45: [-1, 2],
    60: [-1, 3],
    75: [0, 1],
    90: [1, 3],
    105: [1, 2],
    120: [1, 1],
    135: [2, 1],
    150: [3, 1],
    165: [1, 0],
}

// Help fnctn to backtrack along nodes to get our path (woohoo)
function reconstruct_path(cameFrom, current) {
    let path = [current];

    while (cameFrom.hasOwnProperty(current.id)) {
        path.unshift(current);
        current = cameFrom[current.id];
    }

    return path;
}

/* A_STAR ALGORITHM
    * start: {x, y}
    * goal: {x, y}
    * obstacles: 3D array (x, y, angle)
*/
function A_Star(start, goal, obstacles, width=72, height=108) {
    // distance between nodes (manhattan distance + angle diff)
    let d = (n1, n2) => {
        return Math.abs(n2.y - n1.y) + Math.abs(n2.x - n1.x)  + Math.abs(n2.a - n1.a);
    };

    /* HEURISTIC
        * Far away from mining area = bad
        * Further away from the center (more likely to run into walls) = bad
        * Being turned (you have to turn back + move slower towards goal) = bad
    */
    let h = (n) => {
        let delta = degreeMap[n.a+75];
        return Math.abs(n.y - goal.y) + 5 * Math.abs(goal.x - n.x) + Math.abs(n.a);
    };

    class Node {
        constructor(x, y, a) {
            this.x = x;
            this.y = y;
            this.a = a;
            this.id = this.x * height * 12 + this.y * 12 + ((this.a + 75) / 15);
        }

        getNeighbors() {
            let delta = degreeMap[this.a + 75];
            let neighbors = [];
            neighbors.push(new Node(this.x + delta[0], this.y + delta[1], this.a)); // Move forward
            neighbors.push(new Node(this.x - delta[0], this.y - delta[1], this.a)); // Move backward
            neighbors.push(new Node(this.x, this.y, this.a + 15)); // Turn right
            neighbors.push(new Node(this.x, this.y, this.a - 15)); // Turn left

            return neighbors.filter(n => n.isValid());
        }

        isValid() {
            if (this.x <= 0 || this.x >= width) {
                return false;
            }
            if (this.y <= 0 || this.y >= height) {
                return false;
            }
            if (this.a < -75 || this.a > 90) {
                return false;
            }
            return (!obstacles[this.x][this.y][this.a+75]);
        }
    }

    // Just a {} map with a default value
    class Score {
        constructor() {
            this.scores = {};
            this.default = Infinity;
        }

        setScore(node, value) {
            this.scores[node.id] = value;
        }

        getScore(node) {
            if (this.scores.hasOwnProperty(node.id)) return this.scores[node.id];
            else return this.default;
        }
    }

    let g = new Score();
    let f = new Score();

    start = new Node(start.x, start.y, 0);

    g.setScore(start, 0);
    f.setScore(start, h(start));

    let openSet = new PriorityQueue({ comparator: (a, b) => f.getScore(a) - f.getScore(b) });
    let ids = {}; // Ids of nodes in openSet

    openSet.queue(start);
    ids[start.id] = true;

    cameFrom = {};

    while (openSet.length > 0) {
        let current = openSet.dequeue();
        if (ids.hasOwnProperty(current.id)) delete ids[current.id];

        // End condition
        if (current.y <= goal.y) {
            return reconstruct_path(cameFrom, current);
        }

        for (let neighbor of current.getNeighbors()) {
            tentative_gScore = g.getScore(current) + d(current, neighbor);
            if (tentative_gScore < g.getScore(neighbor)) {
                cameFrom[neighbor.id] = current;
                g.setScore(neighbor, tentative_gScore);
                f.setScore(neighbor, tentative_gScore + h(neighbor));
                if (!ids.hasOwnProperty(neighbor.id)) {
                    ids[neighbor.id] = true;
                    openSet.queue(neighbor);
                }
            }
        }
    }

    return []; // :( no solution
}

module.exports = A_Star;
