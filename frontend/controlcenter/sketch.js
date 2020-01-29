let ws;
let driveSettings, generalSettings, consoleSettings;
let state = 2;
const states = ["Tank Drive", "Arcade Drive", "Autonomous"];
const shortStates = ["TD", "AD", "AI"];


let msgs = [];

ws = {send: outputConsole};

let panels = [];

function setup() {
	// ws = new WebSocket("ws://:8080");
	// ws.onmessage = msg => {
    // 	msgs.push(msg.data);
	// };
	driveSettings = QuickSettings.create(document.body.clientWidth - 300, 0.4 * document.body.clientHeight, "Drive settings")
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

	generalSettings = QuickSettings.create(document.body.clientWidth - 300, 0.4 * document.body.clientHeight + 250, "General settings")
		.addBoolean("Snap panels right", true, window.onresize)
		.addRange("Controller refresh (ms)", 100, 5000, 1500, 100)
		.setWidth(200)
		.setHeight(150)

	consoleSettings = QuickSettings.create(document.body.clientWidth - 300, 0.4 * document.body.clientHeight + 425, "Console")
		.addTextArea("Output")
		.overrideStyle("Output", "backgroundColor", "black")
		.overrideStyle("Output", "color", "white")
		.setWidth(350)
		.setHeight(150)
		.disableControl("Output");

	panels = [generalSettings, driveSettings, consoleSettings];
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
	await new Promise(next => setTimeout(next, generalSettings.getValue("Controller refresh (ms)")));
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
			return send("AD", `${leftY},${leftX}`);
		}
		else {
			let right = 6//await (await fetch("http://localhost:8000/right")).json();
			return send("TD", `${leftY},${right}`);
		}
	} catch(e) {}
}

async function send(name, data) {
	if (data) return ws.send(`${name}:${data}`);
	else return ws.send(name);
}

function outputConsole(output) {
	let prevOutput = consoleSettings.getValue("Output");
	let rightNow = new Date()
	consoleSettings.setValue("Output", `${prevOutput}\n> ${output} (${pad(rightNow.getHours())}:${pad(rightNow.getMinutes())}:${pad(rightNow.getSeconds())})`);
	let outputElem = document.getElementById("Output");
	outputElem.scrollTop = outputElem.scrollHeight;
}

function pad(n) {
	return n < 10 ? "0" + n: n;
}

function draw() {


}

window.onresize = function(event) {
	if (!generalSettings.getValue("Snap panels right")) return;
	for (let panel of panels) {
		let curY = parseInt(panel._panel.style.top.split("px")[0]);
		let curWidth = parseInt(panel._panel.style.width.split("px")[0]);
		panel.setPosition(document.body.clientWidth - curWidth - 50, curY);
	}
};
