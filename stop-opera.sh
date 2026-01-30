#!/bin/bash
# Stop Opera - Stops both backend and frontend
# Usage: ./stop-opera.sh

set -e

echo "🛑 Stopping Opera..."

# Stop backend
if lsof -i :8000 > /dev/null 2>&1; then
    ./opera-control.sh stop > /dev/null 2>&1 || launchctl unload ~/Library/LaunchAgents/com.opera.backend.plist
    echo "✓ Backend stopped"
else
    echo "  Backend not running"
fi

# Stop frontend
if [ -f logs/frontend.pid ]; then
    PID=$(cat logs/frontend.pid)
    if kill -0 $PID 2>/dev/null; then
        kill $PID
        rm logs/frontend.pid
        echo "✓ Frontend stopped"
    else
        echo "  Frontend not running"
        rm logs/frontend.pid
    fi
elif lsof -i :3000 > /dev/null 2>&1; then
    # Find and kill by port
    kill $(lsof -t -i:3000) 2>/dev/null
    echo "✓ Frontend stopped"
else
    echo "  Frontend not running" 
fi

echo "✅ Opera stopped"
