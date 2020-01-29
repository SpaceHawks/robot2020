let ws;
let settings;

let msgs = [];


ws = {send: console.log};

function setup() {
	// ws = new WebSocket("ws://:8080");
	// ws.onmessage = msg => {
    // 	msgs.push(msg.data);
	// };
	settings = QuickSettings.create(document.body.clientWidth - 300, document.body.clientHeight/2, "Robot settings")
		.addButton("Tank Drive", ()=>sendXBOX("TD"))
		.addButton("Arcade Drive", ()=>sendXBOX("AD"))
		.addBoolean("Autonomous", true, () => send("AI"))
		.addButton("STOP", () => send("STOP"))
		.overrideStyle("STOP", "backgroundColor", "red")
		.overrideStyle("STOP", "color", "white")
}

async function sendXBOX(name) {
	try {
		let leftY = await (await fetch("http://localhost:8000/leftY")).json();

		if (name === "AD") {
			leftX = await (await fetch("http://localhost:8000/leftX")).json();
			return send("AD", `${leftY}, ${leftX}`);
		}
		else {
			let right = await (await fetch("http://localhost:8000/right")).json();
			return send("TD", `${leftY}, ${right}`);
		}
	} catch(e) {}
}

function send(name, data) {
	if (data) return ws.send(`${name}:${data}`);
	else return ws.send(name);
}

function draw() {


}
