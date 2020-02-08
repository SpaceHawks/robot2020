const chalk = require("chalk");
let A_Star = require("./a_star.js");
let genObstacles = require("./3Dobstacles.js");

// How many tests?
let runCount = 10000;

let start = {x: 36, y: 90};
let end = {x: 36, y: 10};

// Grid-erize numbers (i.e. 359.5 -> 108)
let five = (n) => Math.round(n/5);

function runAstar() {
    let obs = genObstacles();

    let startTime = Date.now();
    let p = A_Star(start, end, obs);

    return ((Date.now() - startTime) / 1000);
}

let sum = 0;
let max_val = 0;
console.log(chalk.green(`Running ${runCount} pathfinding attempts...`));
for (let i = 0; i < runCount; i++) {
    let time = runAstar();
    sum+=time;
    max_val = Math.max(time, max_val);
    console.log(`Path #${chalk.cyan(i+1)}: (${chalk.yellow(roundDecimal(sum/(i+1), 8))} sec on avg)`);
}
console.log(`${chalk.red("Avg:")} ${chalk.yellow(sum/runCount)} sec\n${chalk.red("Max:")} ${chalk.yellow(max_val)} sec`);

function roundDecimal(n, d) {
    return n.toString().substring(0, d);
}
