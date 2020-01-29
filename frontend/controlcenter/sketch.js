let ws;
let settings;
let state = 2;
const states = ["Tank Drive", "Arcade Drive", "Autonomous"];
const shortStates = ["TD", "AD", "AI"];

let msgs = [];


ws = {send: console.log};

async function sendState() {
	if (state < 2) await sendXBOX(states[state].split(" ").map(n => n[0]).join(""));
	await new Promise(next => setTimeout(next, 1500));
	sendState();
}

function setup() {
	// ws = new WebSocket("ws://:8080");
	// ws.onmessage = msg => {
    // 	msgs.push(msg.data);
	// };
	settings = QuickSettings.create(document.body.clientWidth - 300, document.body.clientHeight/2, "Drive settings")
		.addButton("Tank Drive", ()=>handlePress("TD"))
		.addButton("Arcade Drive", ()=>handlePress("AD"))
		.addButton("Autonomous", () => handlePress("AI"))
		.addButton("STOP", () => handlePress("STOP"))
		.overrideStyle("STOP", "backgroundColor", "red")
		.overrideStyle("STOP", "color", "white")

	for (let state of states) settings.overrideStyle(state, "backgroundColor", "gray");
	settings.overrideStyle(states[state], "backgroundColor", "green");
	sendState()
}

function handlePress(name, args) {
	if (name === "STOP") return send("STOP");

	let newState = shortStates.indexOf(name) === -1 ? state : shortStates.indexOf(name);
	if (newState === state) return;
	handleStateChange(state, newState);

}

function handleStateChange(oldState, newState) {
	settings.overrideStyle(states[oldState], "backgroundColor", "gray");
	settings.overrideStyle(states[newState], "backgroundColor", "green");
	state = newState;
}

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
