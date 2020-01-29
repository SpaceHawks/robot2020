let ws;
let driveSettings, displaySettings;
let state = 2;
const states = ["Tank Drive", "Arcade Drive", "Autonomous"];
const shortStates = ["TD", "AD", "AI"];


let msgs = [];

ws = {send: console.log};

let panels = [];

function setup() {
	// ws = new WebSocket("ws://:8080");
	// ws.onmessage = msg => {
    // 	msgs.push(msg.data);
	// };
	driveSettings = QuickSettings.create(document.body.clientWidth - 300, document.body.clientHeight/2, "Drive settings")
		.addButton("Tank Drive", ()=>handlePress("TD"))
		.addButton("Arcade Drive", ()=>handlePress("AD"))
		.addButton("Autonomous", () => handlePress("AI"))
		.addButton("STOP", () => handlePress("STOP"))
		.overrideStyle("STOP", "backgroundColor", "red")
		.overrideStyle("STOP", "color", "white")
		.setWidth(200)
		.setHeight(225);
	for (let state of states) driveSettings.overrideStyle(state, "backgroundColor", "gray");
	driveSettings.overrideStyle(states[state], "backgroundColor", "green");

	displaySettings = QuickSettings.create(document.body.clientWidth - 300, document.body.clientHeight/2 + 225, "Display settings")
		.addBoolean("Snap panels right", true, window.onresize)
		.addRange("Controller refresh (ms)", 100, 5000, 1500, 100)
		.setWidth(200)
		.setHeight(150)

	panels = [displaySettings, driveSettings];
	createCanvas(360, 540);
	background(51);
	window.onresize();
	sendState();
}

function handlePress(name, args) {
	if (name === "STOP") {
		handleStateChange(state, -1);
		return send("STOP");
	}

	let newState = shortStates.indexOf(name) === -1 ? state : shortStates.indexOf(name);
	if (newState === state) return;
	handleStateChange(state, newState);
	if (newState < 2) return sendXBOX(name);
	else if (newState === 2) return send(name);
}

// Async loop to send Arcade/Tank Drive commands
async function sendState() {
	if (state >= 0 && state < 2) await sendXBOX(states[state].split(" ").map(n => n[0]).join(""));
	await new Promise(next => setTimeout(next, displaySettings.getValue("Controller refresh (ms)")));
	sendState();
}

// Changes color of buttons
function handleStateChange(oldState, newState) {
	driveSettings.overrideStyle(states[oldState], "backgroundColor", "gray");
	if (newState >= 0) driveSettings.overrideStyle(states[newState], "backgroundColor", "green");
	state = newState;
}

// Makes the appropriate requests for Arcade/Tank Drive
async function sendXBOX(name) {
	try {
		let leftY = 2//await (await fetch("http://localhost:8000/leftY")).json();

		if (name === "AD") {
			leftX = 5//await (await fetch("http://localhost:8000/leftX")).json();
			return send("AD", `${leftY}, ${leftX}`);
		}
		else {
			let right = 6//await (await fetch("http://localhost:8000/right")).json();
			return send("TD", `${leftY}, ${right}`);
		}
	} catch(e) {}
}

async function send(name, data) {
	if (data) return ws.send(`${name}:${data}`);
	else return ws.send(name);
}

function draw() {


}

window.onresize = function(event) {
	if (!displaySettings.getValue("Snap panels right")) return;
	for (let panel of panels) {
		let curY = parseInt(panel._panel.style.top.split("px")[0]);
		let curWidth = parseInt(panel._panel.style.width.split("px")[0]);
		panel.setPosition(document.body.clientWidth - curWidth - 50, curY);
	}
};
