const ws = new WebSocket("ws://localhost:8080");
ws.onmessage = msg => {
    console.log(msg.data);
}
