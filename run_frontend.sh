#!/bin/bash
cd frontend
x-terminal-emulator -e "sudo node xbox_server.js"
cd controlcenter
x-terminal-emulator -e "http-server -c-1 -o"
