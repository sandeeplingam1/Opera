#!/bin/bash
# Quick Start Opera - Starts both backend and frontend
# Usage: ./start-opera.sh

set -e

echo "🚀 Starting Opera..."

# Check if backend is already running
if lsof -i :8000 > /dev/null 2>&1; then
    echo "✓ Backend already running on port 8000"
else
    echo "Starting backend service..."
    ./opera-control.sh start > /dev/null 2>&1 || launchctl load ~/Library/LaunchAgents/com.opera.backend.plist
    echo "✓ Backend starting... (model loading ~30s)"
fi

# Check if frontend is already running  
if lsof -i :3000 > /dev/null 2>&1; then
    echo "✓ Frontend already running on port 3000"
else
    echo "Starting frontend..."
    cd opera-frontend
    nohup npm run dev -- --hostname 0.0.0.0 > ../logs/frontend.log 2>&1 &
    echo $! > ../logs/frontend.pid
    cd ..
    echo "✓ Frontend started"
fi

echo ""
echo "✅ Opera is ready!"
echo ""
echo "📱 Access from your iPhone:"
echo "   1. Find your Mac's IP: ifconfig | grep 'inet ' | grep -v 127.0.0.1"
echo "   2. Open Safari: http://YOUR_MAC_IP:3000"
echo ""
echo "🎮 Commands:"
echo "   ./stop-opera.sh  - Stop all services"
echo "   ./opera-control.sh status - Check service status"
