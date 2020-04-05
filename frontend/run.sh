#!/usr/bin/sh

# serve frontend on localhost:3030
http-server ./controlcenter -p3030 &

# open in browser
chromium "http://localhost:3030"
