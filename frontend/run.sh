#!/usr/bin/sh

# serve frontend on localhost:3030
http-server ./controlcenter -p3030 &

# run xbox server
x-terminal-emulator -e "sudo node ./xbox_server/xbox_server.js" &

# open in browser
chromium "http://localhost:3030"
