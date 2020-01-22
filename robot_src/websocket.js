// localhost should be replaced with the robot's IP address
const ws = new WebSocket("ws://localhost:8080");
ws.onmessage = msg => {
    console.log(msg.data);
}
